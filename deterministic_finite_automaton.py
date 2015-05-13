class DeterministicFiniteAutomaton():

    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self._states = states  #set of States
        self._alphabet = alphabet #set of letters
        self._transitions = transitions #dict of State:{dict letter:State}
        self._initial_state = initial_state #State
        self._final_states = final_states #set of States

    def insert_state(self, state):
        self._states.add(state)
        self._transitions[state] = {}

    def state_quantity(self):
        return len(self._states)

    def insert_transition(self, source, letter, destiny):
        if(source not in self._states or destiny not in self._states):
            raise Exception("State does not belong to finite automaton")
        self._transitions[source][letter] = destiny

    def has_transition(self, source, letter, destiny):
        return destiny is self._transitions[source][letter]

    def recognize_sentence(self, sentence):
        actual_state = self._initial_state
        for letter in sentence:
            if letter in self._transitions[actual_state]:
                actual_state = self._transitions[actual_state][letter]
            else:
                return False
        return actual_state in self._final_states

    def remove_unreachable(self):
        reachable = self.find_reachable()
        for state in self._states - reachable:
            self.remove_state(state)

    def remove_state(self, remove_state):
        for state in self._states:
            transitions = self._transitions[state].copy()
            for letter in transitions:
                if self._transitions[state][letter] is remove_state:
                    del self._transitions[state][letter]
        del self._transitions[remove_state]
        self._states.remove(remove_state)

    def find_reachable(self):
        actual_size = 0
        reachable_state = {self._initial_state}
        while len(reachable_state) != actual_size:
            actual_size = len(reachable_state)
            temp = set()
            for state in reachable_state:
                through_actual = list(self._transitions[state].values()) #list of states reachable through the actual state
                temp.update(through_actual)
            reachable_state = temp.union({self._initial_state})
        return reachable_state

class State():

    def __init__(self, name):
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other._name

    def __repr__(self):
        return self._name
