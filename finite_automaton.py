import copy

class FiniteAutomaton():

    def __init__(self, states, alphabet, initial_state, final_states):
        self._states = states  #set of States
        self._alphabet = alphabet #set of letters
        self._transitions = {} #dict of State:{dict letter:set of States}
        self._initial_state = initial_state #State
        self._final_states = final_states #set of States
        self._epsilon = '&'
        self._alphabet.add(self._epsilon)
        for state in self._states:
            self._transitions[state] = {}
            for letter in self._alphabet:
                self._transitions[state][letter] = set()

    def insert_state(self, state):
        self._states.add(state)
        self._transitions[state] = {}
        for letter in self._alphabet:
            self._transitions[state][letter] = set()

    def state_quantity(self):
        return len(self._states)

    def is_nondeterministic(self):
        for state in self._states:
            for letter in self._alphabet:
                if len(self._transitions[state][letter]) > 1:
                    return True
        return False

    def insert_transition(self, source, letter, destiny):
        if source not in self._states or destiny not in self._states:
            raise Exception("State does not belong to finite automaton")
        if letter not in self._alphabet:
            raise Exception("Letter does not belong to alphabet")
        self._transitions[source][letter].add(destiny)

    def has_transition(self, source, letter, destiny):
        try:
            return destiny in self._transitions[source][letter]
        except KeyError:
            return False

    def recognize_sentence(self, sentence):
        if not self.is_nondeterministic():
            return self._recognize_sentence_deterministic(sentence)
        return self._recognize_sentence_nondeterministic(sentence, self._initial_state)

    def _recognize_sentence_nondeterministic(self, sentence, actual_state):
        if sentence is "" and self._transitions[actual_state][self._epsilon] == set() :
            return actual_state in self._final_states
        if sentence[0] not in self._alphabet:
            return False
        for state in self._transitions[actual_state][sentence[0]]:
            if self._recognize_sentence_nondeterministic(sentence[1:], state):
                return True
        return False

    def _recognize_sentence_deterministic(self, sentence):
        actual_state = self._initial_state
        for letter in sentence:
            if letter in self._alphabet and len(self._transitions[actual_state][letter]) > 0:
                actual_state = next(iter(self._transitions[actual_state][letter]))
            else:
                return False
        return actual_state in self._final_states

    def remove_unreachable_states(self):
        reachable = self.find_reachable()
        for state in self._states - reachable:
            self.remove_state(state)

    def remove_state(self, remove_state):
        for state in self._states:
            transitions = self._transitions[state].copy()
            for letter in transitions:
                if remove_state in self._transitions[state][letter]:
                    self._transitions[state][letter].remove(remove_state)
        del self._transitions[remove_state]
        self._states.remove(remove_state)

    def find_reachable(self):
        actual_size = 0
        reachable_state = {self._initial_state}
        while len(reachable_state) != actual_size:
            actual_size = len(reachable_state)
            temp = set()
            for state in reachable_state:
                #list of states reachable through the actual state
                through_actual = set()
                for letter in self._transitions[state]:
                    through_actual.update(self._transitions[state][letter])
                temp.update(through_actual)
            reachable_state = temp.union({self._initial_state})
        return reachable_state

    def remove_dead_states(self):
        dead = self._find_dead_states()
        for state in dead:
            self.remove_state(state)

    def _find_dead_states(self):
        alive = self._final_states.copy()
        old = set()
        while alive != old:
            old = alive.copy()
            for state in self._states:
                for letter in self._alphabet:
                    if not self._transitions[state][letter].isdisjoint(alive):
                        alive.add(state)
        return self._states - alive

    def union(self, other):
        old_states = [self._states, other._states]
        old_transitions = [self._transitions, other._transitions]
        old_final_states = [self._final_states, other._final_states]
        states = set()
        transitions = {}
        #dict of State:State where it represents old_state:new_state
        converter = {}
        for i in [0, 1]:
            for old_state in old_states[i]:
                new_state = State(old_state._name + str(i))
                states.add(new_state)
                transitions[new_state] = {}
                converter[old_state] = new_state
        import pdb
        alphabet = self._alphabet.union(other._alphabet)
        final_states = self._final_states.union(other._final_states)
        initial = State("initial")
        states.add(initial)
        automaton = FiniteAutomaton(states, alphabet, initial, final_states)
        #translate transitions to new name of each state
        for i in [0, 1]:
            for old_source in old_transitions[i]:
                for letter in old_transitions[i][old_source]:
                    new_source = converter[old_source]
                    transitions[new_source][letter] = set()
                    for old_destiny in old_transitions[i][old_source][letter]:
                        new_destiny = converter[old_destiny]
                        automaton.insert_transition(new_source, letter, new_destiny)
            for state in old_final_states[i]:
                automaton._final_states.remove(state)
                automaton._final_states.add(converter[state])

        #copy old initial states transitions to new initial state
        for to_copy in {self, other}:
            for letter in to_copy._alphabet:
                for destiny in to_copy._transitions[to_copy._initial_state][letter]:
                    automaton.insert_transition(initial, letter, converter[destiny])
        if self._initial_state in self._final_states or other._initial_state in other._final_states:
            automaton._final_states.add(initial)
        return automaton

    def __repr__(self):
        return str(self._alphabet) + str(self._states) + str(self._transitions) + str(self._final_states)

class State():

    def __init__(self, name):
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other._name

    def __repr__(self):
        return self._name
