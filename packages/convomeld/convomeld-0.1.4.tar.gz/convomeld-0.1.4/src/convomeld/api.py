from typing import Optional, Union, TextIO
from convomeld.parsers import ScriptParser
from convomeld.matchers import ActionMatcher, TriggerValueMatcher
from convomeld.graph import ConvoGraph


def script_to_graph(
    script: list[str], 
    bot_name: str = 'bot', 
    convo_name: str = 'convo_name',
    convo_description: str = 'empty',
    nlp: str = 'exact'
) -> list[dict]:
    """Converts a human readable 'theater' script or conversation log to convoscript graph in v2 format
    >>> # Normal script
    >>> script_to_graph([
    ...     'bot: Hi!', 'bot: Is there anything I can help?', 'human: What time is it now?', 'bot: It is 12PM now', 'bot: Is there anything I can help?', 'human: No', 'bot: Fine, have a good day!'
    ... ])
    [{'name': 'start', 'convo_name': 'convo_name', 'convo_description': 'empty', 'nlp': 'exact', 'actions': {}, 'triggers': {'en': {'__next__': 'convo_name/hint_1'}}}, {'name': 'convo_name/hint_1', 'actions': {'en': ['Hi!']}, 'triggers': {'en': {'__next__': 'convo_name/question_1_1'}}}, {'name': 'convo_name/question_1_1', 'level': 1, 'repeat': 1, 'actions': {'en': ['Is there anything I can help?']}, 'triggers': {'en': {'__default__': 'convo_name/question_1_1', 'What time is it now?': 'convo_name/hint_2'}}}, {'name': 'convo_name/hint_2', 'actions': {'en': ['It is 12PM now']}, 'triggers': {'en': {'__next__': 'convo_name/question_1_2'}}}, {'name': 'convo_name/question_1_2', 'level': 1, 'repeat': 2, 'actions': {'en': ['Is there anything I can help?']}, 'triggers': {'en': {'__default__': 'convo_name/question_1_2', 'No': 'convo_name/hint_3'}}}, {'name': 'convo_name/hint_3', 'actions': {'en': ['Fine, have a good day!']}, 'triggers': {'en': {'__next__': 'stop'}}}, {'name': 'stop', 'actions': {}, 'triggers': {'en': {'__default__': 'start'}}}]
    >>> # Human stop early script
    >>> script_to_graph([
    ...     'bot: Hi!', 'bot: Is there anything I can help?', 'human: What time is it now?', 'bot: It is 12PM now', 'bot: Is there anything I can help?'
    ... ])
    [{'name': 'start', 'convo_name': 'convo_name', 'convo_description': 'empty', 'nlp': 'exact', 'actions': {}, 'triggers': {'en': {'__next__': 'convo_name/hint_1'}}}, {'name': 'convo_name/hint_1', 'actions': {'en': ['Hi!']}, 'triggers': {'en': {'__next__': 'convo_name/question_1_1'}}}, {'name': 'convo_name/question_1_1', 'level': 1, 'repeat': 1, 'actions': {'en': ['Is there anything I can help?']}, 'triggers': {'en': {'__default__': 'convo_name/question_1_1', 'What time is it now?': 'convo_name/hint_2'}}}, {'name': 'convo_name/hint_2', 'actions': {'en': ['It is 12PM now']}, 'triggers': {'en': {'__next__': 'convo_name/question_1_2'}}}, {'name': 'convo_name/question_1_2', 'level': 1, 'repeat': 2, 'actions': {'en': ['Is there anything I can help?']}, 'triggers': {'en': {'__timeout__': 'stop', '__default__': 'convo_name/question_1_2'}}}, {'name': 'stop', 'actions': {}, 'triggers': {'en': {'__default__': 'start'}}}]
    >>> # Bot stop early script
    >>> script_to_graph([
    ...     'bot: Hi!', 'bot: Is there anything I can help?', 'human: No'
    ... ])
    [{'name': 'start', 'convo_name': 'convo_name', 'convo_description': 'empty', 'nlp': 'exact', 'actions': {}, 'triggers': {'en': {'__next__': 'convo_name/hint_1'}}}, {'name': 'convo_name/hint_1', 'actions': {'en': ['Hi!']}, 'triggers': {'en': {'__next__': 'convo_name/question_1_1'}}}, {'name': 'convo_name/question_1_1', 'level': 1, 'repeat': 1, 'actions': {'en': ['Is there anything I can help?']}, 'triggers': {'en': {'__default__': 'convo_name/question_1_1', 'No': 'stop'}}}, {'name': 'stop', 'actions': {}, 'triggers': {'en': {'__default__': 'start'}}}]
    """

    graph = ConvoGraph.from_script_lines(script, convo_name=convo_name, convo_description=convo_description, nlp=nlp, base_author=bot_name, use_uuid=False)
    return graph.to_states_list()


def compare_graphs(graph1: list[dict], graph2: list[dict]) -> bool:
    """Compares a couple of convoscript graphs
    >>> # Normal script
    >>> graph1 = script_to_graph([
    ...     'bot: Hi!', 'bot: Is there anything I can help?', 'human: What time is it now?', 'bot: It is 12PM now', 'bot: Is there anything I can help?', 'human: No', 'bot: Fine, have a good day!'
    ... ])
    >>> compare_graphs(graph1, graph1)
    True
    >>> graph2 = script_to_graph([
    ...     'bot: Hi!', 'bot: Is there anything I can help?', 'human: No', 'bot: Fine, have a good day!'
    ... ])
    >>> compare_graphs(graph1, graph2)
    False
    """

    return ConvoGraph.from_states_list(graph1).compare(ConvoGraph.from_states_list(graph2))


def file_to_graph(
    fp: Union[str, TextIO], 
    convo_name: Optional[str] = None,
    convo_description: Optional[str] = None,
    nlp: Optional[str] = None,
    text_script_parser: Optional[ScriptParser] = None, 
    base_author: Optional[str] = None,
    action_matcher: Optional[ActionMatcher] = None,
    trigger_matcher: Optional[TriggerValueMatcher] = None,
    use_uuid: Optional[bool] = None
) -> list[dict]:
    graph = ConvoGraph.from_file(
        fp,
        convo_name,
        convo_description,
        nlp,
        text_script_parser, 
        base_author,
        action_matcher, 
        trigger_matcher,
        use_uuid
    )
    return graph.to_states_list()


def merge_graphs(*graphs: list[dict], convo_name: Optional[str] = None, convo_description: Optional[str] = None, nlp: Optional[str] = None) -> list[dict]:
    base_graph = None

    if len(graphs) == 0:
        return []

    for graph in graphs:
        if base_graph is None:
            base_graph = ConvoGraph.from_states_list(graph, convo_name=convo_name, convo_description=convo_description, nlp=nlp, use_uuid=False)
        else:
            base_graph = base_graph.merge_graph(ConvoGraph.from_states_list(graph, use_uuid=False))

    return base_graph.to_states_list()