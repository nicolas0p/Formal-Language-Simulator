import copy

class Grammar():

    def __init__(self):
        self._productions = set()

    def productions(self):
        return copy.deepcopy(self._productions)

    def add_production(self, production):
        self._productions.add(production)

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
