import copy

import pdb

class FiniteAutomaton():

    def __init__(self, states, alphabet, initial_state, final_states):
        self._states = states.copy()  #set of States
        self._alphabet = alphabet.copy() #set of letters
        self._transitions = {} #dict of State:{dict letter:set of States}
        self._initial_state = initial_state.copy() #State
        self._final_states = final_states.copy() #set of States
        self._epsilon = '&'
        self._alphabet.add(self._epsilon)
        for state in self._states:
            self._transitions[state] = {}
            for letter in self._alphabet:
                if len(letter) != 1:
                    raise Exception("Alphabet members must be size one only!")
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

    def remove_transition(self, source, letter, destiny):
        try:
            self._transitions[source][letter].remove(destiny)
        except KeyError:
            return

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
        old_transitions = [self._transitions, other._transitions]
        states = set()
        transitions = {}
        number = {self:0, other:1}
        final_states = set()
        #dict of State:State where it represents old_state:new_state
        converter = [{}, {}]
        #translate states to new states
        for current in [self, other]:
            i = number[current]
            for old_state in current._states:
                new_state = State(old_state._name + str(i))
                states.add(new_state)
                transitions[new_state] = {}
                converter[i][old_state] = new_state
                if old_state in current._final_states:
                    final_states.add(converter[i][old_state])
        alphabet = self._alphabet.union(other._alphabet)
        initial = State("initial")
        states.add(initial)
        automaton = FiniteAutomaton(states, alphabet, initial, final_states)
        #translate transitions to new name of each state
        for current in [self, other]:
            i = number[current]
            for old_source in old_transitions[i]:
                for letter in old_transitions[i][old_source]:
                    new_source = converter[i][old_source]
                    transitions[new_source][letter] = set()
                    for old_destiny in old_transitions[i][old_source][letter]:
                        new_destiny = converter[i][old_destiny]
                        automaton.insert_transition(new_source, letter, new_destiny)

        #copy old initial states transitions to new initial state
        for to_copy in {self, other}:
            i = number[to_copy]
            for letter in to_copy._alphabet:
                for destiny in to_copy._transitions[to_copy._initial_state][letter]:
                    automaton.insert_transition(initial, letter, converter[i][destiny])
        if self._initial_state in self._final_states or other._initial_state in other._final_states:
            automaton._final_states.add(initial)
        return automaton

    def complement(self):
        automaton = self.copy()
        automaton.determinize()
        automaton._add_error_state()
        new_final_states = automaton._states - automaton._final_states
        automaton._final_states = new_final_states
        return automaton

    def _add_error_state(self):
        error_state = State("fi")
        self.insert_state(error_state)
        for state in self._states:
            for letter in self._alphabet - {self._epsilon}:
                if self._transitions[state][letter] == set():
                    self.insert_transition(state, letter, error_state)
        for letter in self._alphabet - {self._epsilon}:
            self._transitions[error_state][letter] = {error_state}
        return error_state

    def intersection(self, other):
        complement1 = self.complement()
        complement2 = other.complement()
        union = complement1.union(complement2)
        final = union.complement()
        return final

    def determinize(self):
        if not self.is_nondeterministic():
            return
        states = set() #will contain the State objects
        multi_states = [] #will contain sets of states, every set will be transformed in a State object
        transitions = {}
        to_be_added = [{self._initial_state}]
        final_states = set()
        while to_be_added != []:
            #adds the multi_states that the states reach in new_states
            for multi_state in to_be_added:
                for letter in self._alphabet:
                    destiny_union = set()
                    for state in multi_state:
                        pluri_destiny = self._transitions[state][letter]
                        destiny_union.update(pluri_destiny)
                    if destiny_union not in to_be_added:
                        to_be_added.append(destiny_union)
            to_be_added = [x for x in to_be_added if x not in multi_states]
            multi_states.extend(to_be_added)

        #Creates a state for each multi_state
        for multi_state in multi_states:
            new_state = State(''.join(sorted([x._name for x in multi_state])))
            states.add(new_state)
            transitions[new_state] = {}
            if self._final_states.intersection(multi_state) != set():
                final_states.add(new_state)
            for letter in self._alphabet:
                destiny_union = set()
                for sub_state in multi_state:
                    pluri_destiny = self._transitions[sub_state][letter]
                    destiny_union.update(pluri_destiny)
                destiny = State(''.join(sorted([x._name for x in destiny_union])))
                transitions[new_state][letter] = {destiny}

        self._states = states
        self._final_states = final_states
        self._transitions = transitions

    def is_empty(self):
        return self._initial_state in self._find_dead_states()

    def copy(self):
        automaton = FiniteAutomaton(self._states.copy(), self._alphabet.copy(), self._initial_state.copy(), self._final_states.copy())
        automaton._transitions = copy.deepcopy(self._transitions)
        return automaton

    def __repr__(self):
        return str(self._alphabet) + str(self._states) + str(self._transitions) + str(self._initial_state)+ str(self._final_states)

'''
    def remove_equivalent_states(self):
        self.determinize()
        error_state = self._add_error_state()
        equivalence_classes = self._find_equivalence_classes()
        q = []
        transitions = {}
        final_states = set()
        for i in range(0, len(equivalence_classes)):
            state = State("q" + str(i))
            q.append(state)
            transitions[state] = {}
            transitions[state][self._epsilon] = set()
        for i in range(0, len(equivalence_classes)):
            #any state in equivalent_class number i
            state = next(iter(equivalence_classes[i]))
            if state in self._final_states:
                final_states.add(q[i])
            for letter in self._alphabet - {self._epsilon}:
                #delta(state, letter, tran_qi)
                tran_qi = next(iter(self._transitions[state][letter]))
                location = [equivalence_classes.index(y) for y in equivalence_classes if tran_qi in y][0]
                #gets the number of the class of tran_qi
                transitions[q[i]][letter] = {q[location]}
        self._states = set(q)
        self._transitions = transitions
        self._final_states = final_states
        self.remove_dead_states()

    def _find_equivalence_classes(self):
        equivalence_classes = [self._final_states.copy(), self._states - self._final_states]
        old = []
        while equivalence_classes != old:
            old = copy.deepcopy(equivalence_classes)
            for clas in old:
                for state1 in clas:
                    for state2 in clas:
                        if not self._are_equivalent_states(state1, state2, old):
                            state2_class = [x for x in equivalence_classes if state2 in x][0]
                            state2_class.remove(state2)
                            equivalence_classes.append({state2})
        return [x for x in equivalence_classes if len(x) > 0]

    def _are_equivalent_states(self, state1, state2, equivalence_classes):
        for letter in self._alphabet - {self._epsilon}:
            tran_state1 = next(iter(self._transitions[state1][letter]))
            tran_state2 = next(iter(self._transitions[state2][letter]))
            one = [x for x in equivalence_classes if tran_state1 in x][0]
            if tran_state2 not in one:
                return False
        return True
'''

class State():

    def __init__(self, name):
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def copy(self):
        return State(self._name)

    def __eq__(self, other):
        return self._name == other._name

    def __lt__(self, other):
        return self._name < other._name

    def __repr__(self):
        return self._name
