import copy

class Grammar():

    def __init__(self, terminals = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'}, nonterminals = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'}, initial_symbol = 'S'):
        self._productions = set()
        self._terminals = terminals
        self._nonterminals = nonterminals
        self._initial_symbol = initial_symbol
        if initial_symbol not in self._nonterminals:
            raise InitialSymbolNotInNonTerminalsSetException

    def productions(self):
        return copy.deepcopy(self._productions)

    def add_production(self, production):
        self._productions.add(production)

    def generate(self, sentencial_form = 'S'):

    def productions_quantity(self):
        return len(self._productions)

class Production():

    def __init__(self, left_side, right_side):
        self._left = left_side
        self._right = right_side

    def left(self):
        return self._left

    def right(self):
        return self._right

class InitialSymbolNotInNonTerminalsSetException(Exception):
    def __init__(self):
        self.args = "The initial symbol is not in the nonterminal set"
