import copy
import pdb

class DeterministicFiniteAutomaton():

    def __init__(self, states, alphabet, initial_state, final_states):
        self._states = states  #set of States
        self._alphabet = alphabet #set of letters
        self._transitions = {} #dict of State:{dict letter:State}
        self._initial_state = initial_state #State
        self._final_states = final_states #set of States
        for state in self._states:
            self._transitions[state] = {}

    def insert_state(self, state):
        self._states.add(state)
        self._transitions[state] = {}

    def state_quantity(self):
        return len(self._states)

    def insert_transition(self, source, letter, destiny):
        if source not in self._states or destiny not in self._states:
            raise Exception("State does not belong to finite automaton")
        if letter not in self._alphabet:
            raise Exception("Letter does not belong to alphabet")
        self._transitions[source][letter] = destiny

    def has_transition(self, source, letter, destiny):
        try:
            return destiny is self._transitions[source][letter]
        except KeyError:
            return False

    def recognize_sentence(self, sentence):
        actual_state = self._initial_state
        for letter in sentence:
            if letter in self._transitions[actual_state]:
                actual_state = self._transitions[actual_state][letter]
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
                #list of states reachable through the actual state
                through_actual = list(self._transitions[state].values())
                temp.update(through_actual)
            reachable_state = temp.union({self._initial_state})
        return reachable_state

    def remove_dead_states(self):
        dead = self.find_dead_states()
        for state in dead:
            self.remove_state(state)

    def find_dead_states(self):
        alive = self._final_states.copy()
        old = set()
        while alive != old:
            old = alive.copy()
            for state in self._states:
                for letter in self._alphabet:
                    if letter in self._transitions[state] and self._transitions[state][letter] in alive:
                        alive.add(state)
        return self._states - alive

    def remove_equivalent_states(self):
        #pdb.set_trace()
        error_state = self._add_error_state()
        equivalence_classes = self._find_equivalent_classes()
        q = []
        transitions = {}
        for i in range(0, len(equivalence_classes)):
            state = State("q" + str(i))
            q.append(state)
            transitions[state] = {}
        for i in range(0, len(equivalence_classes)):
            for letter in self._alphabet:
                #any state in equivalent_class number i
                state = next(iter(equivalence_classes[i]))
                #delta(state, letter, tran_qi)
                tran_qi = self._transitions[state][letter]
                location = [equivalence_classes.index(y) for y in equivalence_classes if tran_qi in y][0]
                #gets the number of the class of tran_qi
                transitions[q[i]][letter] = q[location]
        self._states = set(q)
        self._transitions = transitions
        self.remove_dead_states()

    def _find_equivalent_classes(self):
        equivalence_classes = [self._final_states, self._states - self._final_states]
        old = []
        while equivalence_classes != old:
            old = copy.deepcopy(equivalence_classes)
            for clas in old:
                for state1 in clas:
                    for state2 in clas:
                        if not self._are_equivalent_states(state1, state2, equivalence_classes):
                            state2_class = [x for x in equivalence_classes if state2 in x][0]
                            state2_class.remove(state2)
                            equivalence_classes.append({state2})
        return [x for x in equivalence_classes if len(x) > 0]


    def _are_equivalent_states(self, state1, state2, equivalence_classes):
        for letter in self._alphabet:
            tran_state1 = self._transitions[state1][letter]
            tran_state2 = self._transitions[state2][letter]
            one = [x for x in equivalence_classes if tran_state1 in x][0]
            if tran_state2 not in one:
                return False
        return True

    def _add_error_state(self):
        error_state = State("fi")
        self.insert_state(error_state)
        for state in self._states:
            for letter in self._alphabet:
                if letter not in self._transitions[state]:
                    self.insert_transition(state, letter, error_state)
        return error_state

class State():

    def __init__(self, name):
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other._name

    def __repr__(self):
        return self._name
