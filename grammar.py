import copy
from finite_automaton import State
from finite_automaton import FiniteAutomaton

class Grammar():

    def __init__(self, terminals = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', '&'}, nonterminals = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'}, initial_symbol = 'S'):
        self._productions = set()
        self._terminals = terminals
        self._nonterminals = nonterminals
        self._initial_symbol = initial_symbol
        if initial_symbol not in self._nonterminals:
            raise InitialSymbolNotInNonTerminalsSetException

    def productions(self):
        return copy.deepcopy(self._productions)

    def add_production(self, production):
        if production.left() not in self._nonterminals:
            raise Exception("Left side of production not a nonterminal")
        terminal = production.right()[0] in self._terminals
        nonterminal = len(production.right()) == 1
        if len(production.right()) == 2:
            nonterminal = production.right()[1] in self._nonterminals
        if not terminal or not nonterminal:
            raise Exception("Right side is not regular")
        self._productions.add(production)

    def productions_quantity(self):
        return len(self._productions)

    def to_finite_automaton(self):
        # get initial state as the initial symbol
        initial_state = State(self._initial_symbol)
        # create a 'final' state that will get the productions that go just for a terminal
        # as "A->a" or "A->b"
        final_state = State('final')

        # sets for the states and final states
        states = set()
        final_states = set()

        # add the initial and 'final' states to the sets
        states.add(initial_state)
        states.add(final_state)
        final_states.add(final_state)

        # dict that translates a nonterminal to a state, and add the initial state on it
        nonterminals_states = dict()
        nonterminals_states[self._initial_symbol] = initial_state

        # gather states and final states from the existing productions
        for production in self._productions:
            # verify that there is a state for certain nonterminal(on the left)
            # otherwise create it, and add to the states set and dict
            if production._left not in nonterminals_states:
                new_state = State(production._left)
                states.add(new_state)
                nonterminals_states[production._left] = new_state

            # if the nonterminal have a epsilon production, than its state is final
            # as "A->&" or "B->&"
            if production._right == '&':
                state = nonterminals_states[production._left]
                final_states.add(state)

        #print("initial_state",initial_state)
        #print("states",states)
        #print("final_states",final_states)
        #print("nonterminals_states",nonterminals_states)

        # create a ndfa from the states, terminals, initial state and final states gathered above
        ndfa = FiniteAutomaton(states, self._terminals, initial_state, final_states)

        # create the transitions from the productions
        for production in self._productions:
            # get the state correspondent to the nonterminal(on the left)
            state = nonterminals_states[production._left]

            # if the production is in the format "A->a", "A->b"
            # its state gonna have a transition to the 'final' state by its terminal
            if production._right in self._terminals:
                ndfa.insert_transition(state, production._right, final_state)
                #print(production._left, '--', production._right, '->', '[F]')
            # if the production is in the format "A->A", "A->B" ## PS: its not regular ##
            # its state gonna have a transition by epsilon to the other's state
            elif production._right in self._nonterminals:
                other_state = nonterminals_states[production._right]
                ndfa.insert_transition(state, '&', other_state)
                #print(production._left, '--', '&', '->', production._left)
            # if the production is in the format "A->aA", "A->aB"
            # its state gonna have a transition by the terminal to the other nonterminal's state
            elif production._right[0] in self._terminals and production._right[1] in self._nonterminals:
                other_state = nonterminals_states[production._right[1]]
                ndfa.insert_transition(state, production._right[0], other_state)
                #print(production._left, '--', production._right[0], '->', production._right[1])

        # determinize the ndfa and return it
        # ndfa.determinize()
        return ndfa


    def __str__(self):
        productions = {}
        # gather productions of the same left part on a list
        for production in self._productions:
            if production._left not in productions:
                productions[production._left] = []
            productions[production._left].append(production._right)

        string = ''
        # mount string from the gathered productions
        for production in productions.keys():
            string = string + production
            string = string + ' -> '
            for right in productions[production]:
                string = string + right + ' | '
            string = string + '\n'

        return string


    @staticmethod
    def text_to_grammar(text):
        divider = '|'
        grammar = Grammar()
        terminals = set()
        nonterminals = set()
        for line in [a for a in text.split('\n') if a is not ""]:
            left = line.split('->')[0].strip()
            nonterminals.add(left)
            right = line.split('->')[1]
            right = [a.strip() for a in right.split(divider)]
            for symbol in right:
                production = Production(left, symbol)
                grammar.add_production(production)
                terminals.add(symbol[0])
        grammar._terminals = terminals
        grammar._nonterminals = nonterminals
        return grammar


class Production():

    def __init__(self, left_side, right_side):
        self._left = left_side
        self._right = right_side

    def __repr__(self):
        return str(self._left + "->" + self._right)

    def left(self):
        return self._left

    def right(self):
        return self._right

class InitialSymbolNotInNonTerminalsSetException(Exception):
    def __init__(self):
        self.args = "The initial symbol is not in the nonterminal set"
