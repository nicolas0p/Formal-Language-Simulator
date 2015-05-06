class DeterministicFiniteAutomaton():

    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self._states = states
        self._alphabet = alphabet
        self._transitions = transitions
        self._initial_state = initial_state
        self._final_states = final_states

    def insert_state(self, state):
        self._states.add(state)
        self._transitions[state] = set()

    def state_quantity(self):
        return len(self._states)

    def insert_transition(self, source, destiny):
        if(source not in self._states or destiny not in self._states):
            raise Exception("State does not belong to finite automaton")
        self._transitions[source].add(destiny)

    def has_transition(self, source, destiny):
        return destiny in self._transitions[source]

class State():

    def __init__(self, name):
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other._name
