import pandas as pd
import numpy as np
from pathlib import Path
from .constants import DATA_DIR
import sys


DEFAULT_XLSX_PATH = DATA_DIR / 'example_conversation.xlsx'
DEFAULT_FALLBACK_MESSAGE = "Please try again"
DEFAULT_AFFIRMATION = "Good"

# Read spreadsheet and convert to dataframe
def read_and_preprocess_spreadsheet(path):
  # worksheet = gc.open('Test-ActiveListening1').sheet1
  df = pd.read_excel(path, engine='openpyxl')
  df = df.fillna(0)
  script_df = df.replace('', 0)
  script_df['Go to Row Number'] = script_df['Go to Row Number'].apply(np.int64)
  script_df.head()

  return script_df

def TerminalCard(row_num, text = None, next_flow = None):
    message = ''
    if text:
        message = f'''text("""
  {text}
  """)'''
    
    link = ''
    if next_flow :
        link = f'run_stack("{next_flow}")'
        
    terminalCardTemplate=f'''
card Row{row_num} do
  {message}
  
  {link}
end    
    '''
    return terminalCardTemplate


def ContinuingCard(row_num, go_to_row_num, text = None, next_flow = None):
    message = ''
    if text and text != '':
        message = f'''text("""
  {text}
  """)'''

    link = ''
    if next_flow :
        link = f'run_stack("{next_flow}")'
        
    continuingCardTemplate=f'''
card Row{row_num}, then: Row{go_to_row_num} do
  {message}
  
  {link}
end
    '''
    return continuingCardTemplate


def ButtonCard(row_num, go_to_row_nums, text, fallback = None, variable_name = None, variable_action = None):
    # Convert the array of strings to a long string...
    # ...so that Elixir recognizes variables instead of strings
    str = ", ".join(go_to_row_nums)

    fallback_go_to = ''
    fallback_boolean = ''
    if fallback == 'Pass':
        fallback_go_to = f', then: {go_to_row_nums[0]}' 
    elif fallback == 'Reprompt':
        fallback_go_to = f', then: Row{row_num}Fallback'
        fallback_boolean = 'fallback = True'
        
    set_variable = """"""
    if variable_name:
        if variable_name != None and variable_action != None:
            var_name_arr = variable_name.split(',')
            var_action_arr = variable_action.split(',')
            if len(var_name_arr) == len(var_action_arr):
                for i in range(len(var_name_arr)):
                    action = '= 0'
                    if var_action_arr[i] == 'Set 0':
                        action = '= 0'
                    set_variable += f"""
    {var_name_arr[i]} {action}
    """
        
    buttonCardTemplate=f'''
card Row{row_num} {fallback_go_to} do
  {set_variable}
  buttons([{str}]) do
    text("""
    {text}
    """)
  end
  {fallback_boolean}
end    
'''
    return buttonCardTemplate


def ButtonOption(row_num, button_text, go_to_row_num, link = None, variable_name = None, variable_action = None):
    content = 'log("Placeholder")'
    if link:
        content = f'run_stack("{link}")'
    
    go_to = f', then: Row{go_to_row_num}'
    if go_to_row_num == 0:
        go_to = ''
    
    variable = ''
    set_variable = ''
    if variable_name:
        if variable_action == 0 or variable_action is None:
            variable = f'update_contact({variable_name}: "@response")'
        elif variable_action == "Add 1":
            set_variable = f'{variable_name} = {variable_name} + 1'
        elif variable_action == 'Set 0':
            set_variable = f'''
            {variable_name} = {variable_name} + 0
            {variable_name} = {variable_name} + 0
            '''
    buttonOptionTemplate=f'''
card Row{row_num}, "{button_text}" {go_to} do
  {set_variable}

  {content}
  
  {variable}
end
    '''
    return buttonOptionTemplate


def SavedInputCard(row_num, go_to_row_num, prompt, variable_name):
    savedInputCardTemplate=f'''
card Row{row_num}, then: Row{go_to_row_num} do
  response =
    ask("""
    {prompt}
    """)
  update_contact({variable_name}: "@response")
end
'''
    return savedInputCardTemplate


def UnsavedInputCard(row_num, go_to_row_num, prompt, fallback):  
    if fallback:
        next_card = f"Row{row_num}Manager"
    else:
        next_card = f"Row{go_to_row_num}"
    unsavedInputCardTemplate=f'''
card Row{row_num}, then: {next_card} do
  response = ask("""
  {prompt}
  """)
end
'''
    return unsavedInputCardTemplate


def ImageCardWithText(row_num, go_to_row_num, image_link, text):
    ImageTemplate=f'''
card Row{row_num}, then: Row{go_to_row_num} do
  image("{image_link}")

  text("""
  {text}
  """)
end
    '''
    return ImageTemplate


def ImageCardWithButtons(row_num, go_to_row_nums, image_link, text, fallback):
    fallback_boolean = ''
    fallback_go_to = ''
    if fallback == 'Pass':
        fallback_go_to = f', then: {go_to_row_nums[0]}' 
    elif fallback == 'Reprompt':
        fallback_go_to = f', then: Row{row_num}Fallback'
        fallback_boolean = 'fallback = True'

    str = ", ".join(go_to_row_nums)
   
    ImageTemplate=f'''   
card Row{row_num} {fallback_go_to} do
  buttons([{str}]) do
      image("{image_link}")
      text("""
      {text}
      """)
  end
  {fallback_boolean}
end
    '''
    return ImageTemplate


def SkipCard(row_num, go_to_row_num, skip_trigger, variable_name):
    trigger_arr = []
    
    if isinstance(skip_trigger, str):
        trigger_arr.append(f'response == "{skip_trigger.lower()}"')
        trigger_arr.append(f'response == "{skip_trigger.capitalize()}"')
        trigger_arr.append(f'response == "{skip_trigger.upper()}"')
        
        skip_triggers_positive = ' or '.join(trigger_arr)
        
        negative_arr = [x.replace("==","!=") for x in trigger_arr]
        
        skip_triggers_negative = ' and '.join(negative_arr)
        
    
    SkipTemplate=f'''   
card Row{row_num} when {skip_triggers_positive}, then: Row{go_to_row_num} do
  log("Placeholder")
end

card Row{row_num} when {skip_triggers_negative}, then: Row{go_to_row_num} do
  log("Placeholder")
  
  update_contact({variable_name}: "@response")
end
    '''
    return SkipTemplate


def FallbackCard(row_num, fallback_message):
    fallback_card_name = f'Row{row_num}Fallback'
  
    FallbackTemplate = f'''
card {fallback_card_name} when fallback == True, then: Row{row_num} do
  fallback = False
  
  text("""
  {fallback_message}
  """)
end
    '''
    return FallbackTemplate


def InputFallbackCard(row_num, go_to, target_input,
    affirmation=DEFAULT_AFFIRMATION,
    fallback_message=DEFAULT_FALLBACK_MESSAGE):
    # fallback_card_name = f'Row{row_num}Fallback'
  
    FallbackTemplate = f'''
card Row{row_num}Manager when response == {target_input}, then: Row{go_to} do
  text("{affirmation}")
end

card Row{row_num}Manager when fallback != {target_input}, then: Row{row_num} do
  text("""
  {fallback_message}
  """)
end
    '''
    return FallbackTemplate


def select_text_card_format(row_data):
    card = ''
    if row_data['go_to_row_num']:
        card = ContinuingCard(
            row_data['row_num'], 
            row_data['go_to_row_num'], 
            row_data['bot_content'], 
            row_data['link']
        )
    elif row_data['go_to'] == 0 or row_data['go_to'] is False:
        card = TerminalCard(
            row_data['row_num'], 
            row_data['bot_content'], 
            row_data['link']
        )
    return card


def ListMenuCard(row_num, options, text, title, header, footer, fallback = None):
    menu_text = f'text("{text}")'
    menu_header = f'header("{header}")'
    menu_footer = f'footer("{footer}")'
    menu_options = ", ".join(options)

    menuCardTemplate=f'''
card Row{row_num} do
  list("{title}", [{menu_options}]) do
    {menu_text}
    {menu_header}
    {menu_footer}
  end
end
'''
    return menuCardTemplate


def MenuOptionCard(row_num, button_text, go_to_row_num, link = None):
    content = 'log("Placeholder")'
    if link:
        content = f'run_stack("{link}")'
    
    go_to = f', then: Row{go_to_row_num}'
    if go_to_row_num == 0:
        go_to = ''
    
    
    buttonOptionTemplate=f'''
card Row{row_num}, "{button_text}" {go_to} do
  {content}
  
end
    '''
    return buttonOptionTemplate


def select_image_card_format(script_df, index, row_data, skip_row=None):
    """ FIXME: skip_row is unused """
    i = row_data['row_num']
    row_check = True
    while row_check:
        i += 1
        if (script_df.iloc[[i-2]]['Type'] == 'Text').bool():
            text = script_df.loc[i-1]['Bot says']
            go_to = script_df.loc[i-1]['Go to Row Number']

            card = ImageCardWithText(
                row_data['row_num'], 
                go_to, 
                row_data['link'], 
                text
            )
            row_check = False               
            # skip_row = index+1       
        elif (script_df.iloc[[i-2]]['Type'] == 'Button Prompt').bool():
            buttons_arr = []
            j = i
            button_check=True
            text = script_df.loc[j-1]['Bot says']
            fallback = script_df.loc[j-1]['Fallback Strategy']
            # skip_row = index + 1
              
            while button_check:
                j += 1
                # iloc uses a different value than i (-2) because it has header row and Row 2
                if (script_df.iloc[[j-2]]['Type'] == 'Button').bool():                       
                    buttons_arr.append(f"Row{j}")
                else:
                    button_check = False

            if fallback == 0:
                fallback = None
                
            card = ImageCardWithButtons(
                row_data['row_num'], 
                buttons_arr, 
                row_data['link'], 
                text,
                script_df.iloc[0]['Reprompt Fallback Message']
            )

            if fallback == 'Reprompt':
                card += FallbackCard(
                    row_data['row_num'], 
                    script_df.iloc[0]['Reprompt Fallback Message']
                )
                    
            row_check = False

    return card


def select_button_prompt_card_format(script_df, row_data):
    buttons_arr = []
    i = row_data['row_num']
    row_check = True

    while row_check:
        i += 1
        if (script_df.iloc[[i-2]]['Type'] == 'Button').bool():
            buttons_arr.append(f"Row{i}")
        else:
            row_check = False
    
    if not row_data['fallback']:
        row_data['fallback'] = None
            
    if row_data['variable_action'] == 0:
        row_data['variable_action'] = None

    card = ButtonCard(
        row_data['row_num'], 
        buttons_arr, 
        row_data['bot_content'], 
        row_data['fallback'], 
        row_data['variable_name'], 
        row_data['variable_action']
    )  
        
    if row_data['fallback'] == 'Reprompt':
        card += FallbackCard(
            row_data['row_num'],
            row_data['fallback']
        )
        
    return card


def select_button_card_format(row_data):
    if row_data['variable_name'] == 0:
        row_data['variable_name'] = None
        
    if row_data['variable_action'] == 0:
        row_data['variable_action'] = None

    card = ButtonOption(
        row_data['row_num'], 
        row_data['user_content'], 
        row_data['go_to_row_num'], 
        row_data['link'], 
        row_data['variable_name'], 
        row_data['variable_action']
    )

    return card


def select_user_input_card_format(script_df, row_data):
    go_to = script_df.loc[row_data['row_num']+1-2]['Go to Row Number']
        
    next_row_type = script_df.loc[row_data['row_num'] + 2 - 2]['Type']
    next_row_type = next_row_type.lower().strip()

    if next_row_type == 'skip':
        skip_trigger = script_df.loc[row_data['row_num']+2-2]['User says']

        skip_row_num = row_data['row_num'] + 2
        skip_go_to_row = row_data['row_num'] + 3
        go_to = skip_row_num

    fallback = None 
    if row_data['fallback']:
        fallback = row_data['fallback'].lower().strip()
                  
            
    if row_data['variable_name']:
        card = SavedInputCard(
            row_data['row_num'], 
            go_to, 
            row_data['bot_content'], 
            row_data['variable_name']
        )
    else:
        card = UnsavedInputCard(
            row_data['row_num'], 
            go_to, 
            row_data['bot_content'], 
            fallback
        )

    if fallback == 'Reprompt':
        target_input = script_df.loc[row_data['row_num']-1]['User says']
        card += InputFallbackCard(
            row_data['row_num'], 
            go_to, 
            target_input, 
            "Good",   # affirmation
            "Try again"  # fallback_message
        )

    if next_row_type == 'skip':
        card += SkipCard(
            skip_row_num, 
            skip_go_to_row, 
            skip_trigger, 
            row_data['variable_name']
        )
    return card


def select_list_menu_card_format(script_df, row_data):
    # menu_text = row_data['bot_content']
    menu_header = ''
    menu_footer = ''
    menu_title = ''  

    menu_options = []

    menu_option_cards = []

    i = row_data['row_num']
    row_check = True

    while row_check:
        i += 1
        try:
          row_type = script_df.iloc[[i-2]]['Type']
        except:
          break
        if (row_type == 'List Menu Title').bool():
            menu_title = script_df.loc[i-1]['Bot says']
        elif (row_type == 'List Menu Header').bool():
            menu_header = script_df.loc[i-1]['Bot says']
        elif (row_type == 'List Menu Footer').bool():
            menu_footer = script_df.loc[i-1]['Bot says']
        elif (row_type == 'List Menu Option').bool():
            menu_options.append(f"Row{i}")
            menu_option_card = MenuOptionCard(
                i,
                script_df.loc[i-1]['User says'],
                script_df.loc[i-1]['Go to Row Number'],
                script_df.loc[i-1]['Links'],
            )
            menu_option_cards.append(menu_option_card)
        else:
            row_check = False   

    card = ListMenuCard(
        row_data['row_num'],
        menu_options,
        row_data['bot_content'],
        menu_title,
        menu_header,
        menu_footer
    )

    for menu_card in menu_option_cards:
      card += menu_card

    return card


def evaluate_card_type_of_row(script_df, index, row_data):
    if row_data['user_content'] == '<user input>':
        card = ''
    elif row_data['row_type'] == 'Text':
        card = select_text_card_format(row_data)
    elif row_data['row_type'] == 'Image':       
        card = select_image_card_format(script_df, index, row_data)
    elif row_data['row_type'] == 'Button Prompt':
        card = select_button_prompt_card_format(script_df, row_data)
    elif row_data['row_type'] == 'Button':       
        card = select_button_card_format(row_data)
    elif row_data['row_type'] == 'User Input Prompt':   
        card = select_user_input_card_format(script_df, row_data)
    elif row_data['row_type'] == 'List Menu':
        card = select_list_menu_card_format(script_df, row_data)
    else:
        card = ''

    return card


def get_values_for_a_row(index, row):
    row_data = {
        'row_num': index+2, # Index
        'row_type': row['Type'], # Column A
        'bot_content': row['Bot says'], # Column B
        'user_content': row['User says'], # Column C
        'go_to': row['Go to'], # Column D
        'go_to_row_num': row['Go to Row Number'], # Column E
        'variable_name': row['Save to Variable'], # Column F
        'variable_action': row['Variable Action'], # Column G
        'fallback': row['Fallback Strategy'], # Column H
        'link': row['Links'], # Column I
        'notes': row['Notes/comments'], # Column J
        'card_title': f'Row{index+2}'
    }
    return row_data


def loop_through_df_rows(script_df):
    card_arr = []
    for index, row in script_df.iterrows():   
        row_data = get_values_for_a_row(index, row)
        card = evaluate_card_type_of_row(script_df, index, row_data)
        card_arr.append(card.strip())
    return card_arr


def write_file(card_arr):
    with open('refactoring_test.txt','w', encoding="utf-8") as f:
        for card in card_arr:
            if not card.strip():
                continue
            f.write(card.strip() + '\n')
    return '\n'.join(card_arr)








def convert(path=DEFAULT_XLSX_PATH):
    """ Convert xlsx file to Turn.IO Stacks text file """
    script_df = read_and_preprocess_spreadsheet(DEFAULT_XLSX_PATH)
    card_arr = loop_through_df_rows(script_df)
    return write_file(card_arr)


if __name__ == '__main__':
    path = DEFAULT_XLSX_PATH
    if len(sys.argv) > 1:
        path = Path(sys.arg[1])
    print(convert(path=path))
