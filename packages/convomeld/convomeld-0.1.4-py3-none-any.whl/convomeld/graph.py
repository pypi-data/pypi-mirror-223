from __future__ import annotations
from typing import Optional, TextIO, Union, Any
from collections.abc import Sequence
from convomeld.state import Action, State, Trigger, TriggerPlaceholder
from convomeld.thread import ConvoThread
from convomeld.parsers import ScriptParser, SimpleScriptParser
from convomeld.matchers import ActionMatcher, SimpleActionMatcher, TriggerValueMatcher, SimpleTriggerValueMatcher
from convomeld.merge import MergeHandler, MergeValidator, StopEarlyHandler, DefaultTriggerHandler, SubthreadAppendHandler, SubthreadMergeHandler
import os
import yaml
from uuid import uuid4


class ConvoGraph:
    def __init__(
        self, 
        action_matcher: ActionMatcher,
        trigger_matcher: TriggerValueMatcher,
        states: Optional[dict[str, State]] = None, 
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        nlp: Optional[str] = None,
        use_uuid: bool = True
    ) -> None:        
        self._states: dict[str, State] = {}
        self._action_matcher = action_matcher
        self._trigger_matcher = trigger_matcher
        self._uuid = uuid4().hex[-6:]
        self._hint_state_count = 0
        self._use_uuid = use_uuid
        self._merge_handlers: list[MergeHandler] = [
            MergeValidator(self._trigger_matcher),
            DefaultTriggerHandler(self._trigger_matcher),
            SubthreadMergeHandler(self._action_matcher, self._trigger_matcher),
            SubthreadAppendHandler(self._trigger_matcher),
            StopEarlyHandler(self._trigger_matcher),
            MergeValidator(self._trigger_matcher),
        ]

        if states is None:
            if convo_name is None:
                raise RuntimeError('convo_name must be provided')
            if convo_description is None:
                convo_description = 'empty'
            if nlp is None:
                nlp = 'exact'

            states = {
                'start': State('start', triggers=[TriggerPlaceholder.timeout().create_trigger('stop')], convo_name=convo_name, convo_description=convo_description, nlp=nlp),
                'stop': State('stop', triggers=[TriggerPlaceholder.default().create_trigger('start')])
            }

        state_name_mapping = {}

        for state in states.values():
            state_attrs = dict(state.attrs)

            if state.name == 'start':
                if convo_name is not None:
                    state_attrs['convo_name'] = convo_name
                if convo_description is not None:
                    state_attrs['convo_description'] = convo_description
                if nlp is not None:
                    state_attrs['nlp'] = nlp

                state_new_name = state.name
            elif state.name == 'stop':
                state_new_name = state.name
            else:
                if 'level' not in state_attrs and 'repeat' not in state_attrs:
                    self._hint_state_count += 1
                # self._simple_state_count += 1

                state_new_name = self._generate_state_name(level=state_attrs.get('level'), repeat=state_attrs.get('repeat'))
            
            state_name_mapping[state.name] = state_new_name
            self._states[state_new_name] = state.copy(name=state_new_name, **state_attrs)

        for state in self._states.values():
            for trigger in state.triggers:
                trigger.state_name = state_name_mapping[trigger.state_name]

    # Graph section

    def _generate_state_name(self, level: Optional[str] = None, repeat: Optional[str] = None) -> str:
        if self._use_uuid:
            script_prefix = f'script_{self._uuid}'
        else:
            script_prefix = f'{self._states["start"].attrs["convo_name"]}'

        if level is not None and repeat is not None:
            state_name = f'question_{level}_{repeat}'
        else:
            state_name = f'hint_{self._hint_state_count}'
        # state_name = f'state_{self._simple_state_count}'

        return script_prefix + '/' + state_name

    def create_state(self, src: State) -> State:
        if 'level' not in src.attrs and 'repeat' not in src.attrs:
            self._hint_state_count += 1
        # self._simple_state_count += 1

        new_state_name = self._generate_state_name(level=src.attrs.get('level'), repeat=src.attrs.get('repeat'))
        new_state = src.copy(name=new_state_name, triggers=[])
        self._states[new_state.name] = new_state
        return new_state

    def find_state(
        self,
        name: Optional[str]=None,
        actions: Optional[Sequence[Action]]=None,
        many: bool=False,
        **attrs
    ) -> Union[Optional[State], Sequence[State]]:
        if name is not None:
            states = [self._states[name]] if name in self._states else []
        else:
            states = list(self._states.values())

        for attr_name, attr_value in attrs.items():
            states = [state for state in states if attr_name in state.attrs and state.attrs[attr_name] == attr_value]

        if actions is not None:
            states = [state for state in states if self._action_matcher.match(state.actions, actions)]

        if many:
            return states
        else:
            return states[0] if len(states) else None
        
    def num_states(self) -> int:
        return len(self._states)
        
    def _merge_next_subthread(self, current_state: State, tp: TriggerPlaceholder, next_subthread: ConvoThread, merge_state: Optional[State]) -> State:
        # current_state: already existing State of the ConvoGraph
        # tp: generates trigger to connect existing state with the next_subthread
        # next_subthread: follows trigger generated from tp, can be merged with already existing "next subthreads" triggered from current_state
        # merge_state: final state which is the end of next_subthread, should be created if is None, can be already existing State, can also equal current_state

        for merge_handler in self._merge_handlers:
            merge_handler_result = merge_handler.merge(self, current_state, tp, next_subthread, merge_state)

            if merge_handler_result is not None:
                # merge_state <- merge_handler_result
                if merge_state is not None and merge_handler_result is not merge_state:
                    raise RuntimeError(f'Merge error: merge_handler_result {merge_handler_result} is expected to be target merge_state f{merge_state}')

                merge_state = merge_handler_result 

        if merge_state is None:
            raise RuntimeError('Merge error: merge_state is None after all merge handlers')

        return merge_state

    def merge_thread(self, thread: ConvoThread) -> ConvoGraph:
        if not thread.get_first_state().attrs.get('is_start', False):
            raise RuntimeError('Merge error: target thread must begin with "start" state')
        if not thread.get_last_state().attrs.get('is_stop', False):
            raise RuntimeError('Merge error: target thread must end with "stop" state')
        # Pop "start" state
        thread.pop_first_state()

        current_state = self._states['start']
        current_tp = TriggerPlaceholder.next()
        level = 0
        repeat = 0

        next_subthread = ConvoThread()

        for state, prev_trigger in thread.iter_states(with_prev_trigger=True):        
            state_attrs = dict(state.attrs)

            if len(state.triggers) == 0:
                next_subthread.append_state(state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **state_attrs)
                self._merge_next_subthread(current_state, current_tp, next_subthread, self._states['stop'])
                continue

            state_trigger = state.triggers[0]
            current_state_match = self._action_matcher.match(current_state.actions, state.actions)

            if not state.triggers[0].is_next() or current_state_match:
                if 'level' in state_attrs:
                    level = state_attrs['level']
                else:
                    if not current_state_match:
                        level += 1
                    state_attrs['level'] = level
                if 'repeat' in state_attrs:
                    repeat = state_attrs['repeat']
                else:
                    if current_state_match:
                        repeat += 1
                    else:
                        repeat = 1
                    state_attrs['repeat'] = repeat

            next_subthread.append_state(state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **state_attrs)
            merge_state = self.find_state(actions=state.actions, repeat=state_attrs.get('repeat'), level=state_attrs.get('level'))

            if state_trigger.is_next():
                if current_state_match:
                    state_trigger = TriggerPlaceholder.timeout().create_trigger(state_trigger.state_name)
                else:
                    continue

            current_state = self._merge_next_subthread(current_state, current_tp, next_subthread, merge_state)
            current_tp = TriggerPlaceholder.from_trigger(state_trigger)
            next_subthread = ConvoThread()

        return self

    def to_threads(self) -> list[ConvoThread]:
        start_state = self._states['start']

        complete_threads = []
        state_queue: list[tuple[State, ConvoThread, set[State]]] = [
            (start_state, ConvoThread().append_state(start_state.actions, TriggerPlaceholder.none(), **start_state.attrs, is_start=True), set())
        ]

        while len(state_queue):
            current_state, thread, processed_states = state_queue.pop(0)

            if current_state in processed_states:
                continue
            if current_state.name == 'stop':
                complete_threads.append(thread)
                continue

            next_subthreads: list[tuple[Trigger, ConvoThread, State]] = []

            for trigger in current_state.triggers:
                state = self._states[trigger.state_name]
                state_attrs = {**state.attrs, 'is_start': True} if state.name == 'start' else {**state.attrs, 'is_stop': True} if state.name == 'stop' else state.attrs
                subthread_states = ConvoThread().append_state(state.actions, TriggerPlaceholder.none(), **state_attrs)

                while state.find_trigger(TriggerPlaceholder.next(), self._trigger_matcher) is not None:
                    prev_trigger = state.triggers[0]
                    state = self._states[prev_trigger.state_name]
                    state_attrs = {**state.attrs, 'is_start': True} if state.name == 'start' else {**state.attrs, 'is_stop': True} if state.name == 'stop' else state.attrs
                    subthread_states.append_state(state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **state_attrs)
                
                if state is not current_state:
                    # Trigger doesn't lead to loopback
                    next_subthreads.append((trigger, subthread_states, state))
                    continue

                # Trigger leads to a loopback
                for subthread_state, prev_trigger in subthread_states.iter_states(with_prev_trigger=True):
                    if prev_trigger.is_none():
                        prev_trigger = trigger
                    thread.append_state(subthread_state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **subthread_state.attrs)

            processed_states.add(current_state)
            
            for trigger, subthread_states, state in next_subthreads:
                next_thread = thread.copy()

                for subthread_state, prev_trigger in subthread_states.iter_states(with_prev_trigger=True):
                    if prev_trigger.is_none():
                        prev_trigger = trigger
                    next_thread.append_state(subthread_state.actions, TriggerPlaceholder.from_trigger(prev_trigger), **subthread_state.attrs)
                
                state_queue.append((state, next_thread, processed_states.copy()))

        return complete_threads

    def merge_graph(self, graph: ConvoGraph) -> ConvoGraph:
        result = self

        for thread in graph.to_threads():
            result = result.merge_thread(thread)

        return result
    
    def compare(self, other: ConvoGraph) -> bool:
        state_queue = [(self._states['start'], other.find_state(name='start'))]
        processed_states = set()

        while len(state_queue):
            state1, state2 = state_queue.pop(0)

            if state1 in processed_states:
                continue
            if (state1.name == 'start') ^ (state2.name == 'start'):
                return False
            if (state1.name == 'stop') ^ (state2.name == 'stop'):
                return False
            if state1.attrs != state2.attrs:
                return False
            if not self._action_matcher.match(state1.actions, state2.actions):
                return False
            if len(state1.triggers) != len(state2.triggers):
                return False
            
            for trigger1 in state1.triggers:
                trigger2 = state2.find_trigger(TriggerPlaceholder.from_trigger(trigger1), self._trigger_matcher)
                
                if trigger2 is None:
                    return False
                
                state_queue.append((self._states[trigger1.state_name], other.find_state(name=trigger2.state_name)))
                
            processed_states.add(state1)

        return True

    # Export section

    def to_states_list(self) -> list:
        stop_state = self._states.pop('stop')
        self._states['stop'] = stop_state
        return [state.to_dict() for state in self._states.values()]
    
    def to_yaml(self, fp: Union[str, TextIO]) -> None:
        if isinstance(fp, str):
            if not fp.endswith('.yml') :
                fp += '.yml'
            dir = os.path.dirname(fp)
            if not os.path.exists(dir):
                os.makedirs(dir)
            fp = open(fp, 'w', encoding='utf-8')

        state_list = self.to_states_list()
        yaml.safe_dump(state_list, fp, sort_keys=False, encoding='utf-8')
        fp.close()

    # Import section

    @classmethod
    def from_states_list(
        cls, 
        states_list: list[dict], 
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        nlp: Optional[str] = None,
        action_matcher: Optional[ActionMatcher] = None, 
        trigger_matcher: Optional[TriggerValueMatcher] = None,
        use_uuid: Optional[bool] = None
    ) -> ConvoGraph:
        states = {
            state_dict['name']: State.from_dict(state_dict)
            for state_dict in states_list
        }

        if action_matcher is None:
            action_matcher = SimpleActionMatcher()
        if trigger_matcher is None:
            trigger_matcher = SimpleTriggerValueMatcher()
        if use_uuid is None:
            use_uuid = True

        graph = cls(action_matcher, trigger_matcher, states, convo_name=convo_name, convo_description=convo_description, nlp=nlp, use_uuid=use_uuid)
        return graph

    @classmethod
    def from_file(
        cls, 
        fp: Union[str, TextIO], 
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        nlp: Optional[str] = None,
        text_script_parser: Optional[ScriptParser] = None, 
        base_author: Optional[str] = None,
        action_matcher: Optional[ActionMatcher] = None,
        trigger_matcher: Optional[TriggerValueMatcher] = None,
        use_uuid: Optional[bool] = None
    ) -> ConvoGraph:
        if isinstance(fp, str) and (fp.endswith('.yml') or fp.endswith('.yaml')):
            return cls.from_yaml_file(fp, action_matcher, trigger_matcher, use_uuid)
        else:
            # Assume text file by default
            return cls.from_text_file(fp, convo_name, convo_description, nlp, text_script_parser, base_author, action_matcher, trigger_matcher, use_uuid)
        
    @classmethod
    def from_yaml_file(
        cls, 
        fp: Union[str, TextIO], 
        action_matcher: Optional[ActionMatcher] = None,
        trigger_matcher: Optional[TriggerValueMatcher] = None, 
        use_uuid: Optional[bool] = None
    ) -> ConvoGraph:
        if isinstance(fp, str): 
            fp = open(fp, 'r', encoding='utf-8')

        script_list = yaml.safe_load(fp)
        fp.close()
        return cls.from_states_list(script_list, action_matcher, trigger_matcher, use_uuid=use_uuid)
    
    @classmethod
    def from_text_file(
        cls, 
        fp: Union[str, TextIO], 
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        nlp: Optional[str] = None,
        script_parser: Optional[ScriptParser] = None, 
        base_author: Optional[str] = None,
        action_matcher: Optional[ActionMatcher] = None,
        trigger_matcher: Optional[TriggerValueMatcher] = None,
        use_uuid: Optional[bool] = None
    ) -> ConvoGraph:
        if isinstance(fp, str): 
            fp = open(fp, encoding='utf-8')

        raw_lines = fp.readlines()
        fp.close()

        return cls.from_script_lines(
            raw_lines,
            convo_name,
            convo_description,
            nlp,
            script_parser,
            base_author,
            action_matcher, 
            trigger_matcher,
            use_uuid
        )
    
    @classmethod
    def from_script_lines(
        cls,
        text_lines: list[str],
        convo_name: Optional[str] = None,
        convo_description: Optional[str] = None,
        nlp: Optional[str] = None,
        script_parser: Optional[ScriptParser] = None,
        base_author: Optional[str] = None,
        action_matcher: Optional[ActionMatcher] = None,
        trigger_matcher: Optional[TriggerValueMatcher] = None,
        use_uuid: Optional[bool] = None
    ) -> ConvoGraph:
        if convo_name is None:
            convo_name = 'convo_name'
        if convo_description is None:
            convo_description = 'empty'
        if nlp is None:
            nlp = 'exact'
        if script_parser is None:
            script_parser = SimpleScriptParser()
        if base_author is None:
            base_author = 'teacher'
        if action_matcher is None:
            action_matcher = SimpleActionMatcher()
        if trigger_matcher is None:
            trigger_matcher = SimpleTriggerValueMatcher()
        if use_uuid is None:
            use_uuid = True

        script_lines = script_parser.parse_lines(text_lines)
        
        graph = cls(action_matcher, trigger_matcher, convo_name=convo_name, convo_description=convo_description, nlp=nlp, use_uuid=use_uuid)
        graph_start_state = graph.find_state(name='start')
        graph_stop_state = graph.find_state(name='stop')

        thread = ConvoThread().append_state(graph_start_state.actions, TriggerPlaceholder.none(), **graph_start_state.attrs, is_start=True)
        tp = None

        for line in script_lines:
            if line.author == base_author:
                action = Action(line.text, line.lang_group)
                thread = thread.append_state(action, tp or TriggerPlaceholder.next())
                tp = None
            else:
                tp = TriggerPlaceholder(line.text, line.lang_group)

        thread = thread.append_state(graph_stop_state.actions, tp or TriggerPlaceholder.next(), **graph_stop_state.attrs, is_stop=True)
        return graph.merge_thread(thread)

