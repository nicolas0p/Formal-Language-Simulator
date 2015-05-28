class RegularExpression:
    def __init__(self, string, terminals = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'}):
        self._string = string
        self._terminals = terminals
        self._normalize()

    # add unseen concatenations
	# ba(na)*na  ==>  b.a.(n.a)*.n.a
    # removes outer unnecessary parenthesis
    # (ab*a) => ab*a
    def _normalize(self):
        string = self._string

        if len(string) == 0:
            return

        pos = 0;
        for i in range(0,len(self._string)-1):
            pair = self._string[i:i+2]

            # "ab" or "a(" or ")a" or "*a" or "*(" or ")("
            if  ( pair[0] in self._terminals and pair[1] in self._terminals ) or \
                ( pair[0] in self._terminals and pair[1] == '(' ) or \
                ( pair[0] == ')' and pair[1] in self._terminals ) or \
                ( pair[0] == '*' and pair[1] in self._terminals ) or \
                ( pair[0] == '*' and pair[1] == '(' ) or \
                ( pair[0] == ')' and pair[1] == '('):

                string = string[:pos+1] + '.' + string[pos+1:]
                pos = pos + 1

            pos = pos + 1

        self._string = string

        # while there is a parenthesis in the front, and in the back of the string,
        # and the method to return the less significant symbol is not returning anything
        # remove the front and back parenthesis
        while ( self._string[0] == '(' and self._string[len(self._string)-1] == ')' ) and \
            ( self._get_less_significant() == ('&',-1) ):

            self._string = self._string[1:len(self._string)-1]

    # returns the less significant symbol from the 'outer level' of the string
    # it ignores everything that is inside parenthesis, so it ignores 'inner levels'
    def _get_less_significant(self):
        level = 0
        less_significant = ('&',-1) # symbol | position
        for i in range(0,len(self._string)):
            char = self._string[i]
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1
            elif level == 0:
                if char == '|' and less_significant[0] != '|':
                    less_significant = ('|',i)
                elif char == '.' and less_significant[0] not in ['|','.']:
                    less_significant = ('.',i)
                elif char == '*' and less_significant[0] not in ['|','.','*']:
                    less_significant = ('*',i)
                elif less_significant[0] not in ['|','.','*']:
                    less_significant = (char,i)

        return less_significant

    def _get_de_simone_tree(self):
        symbol = self._get_less_significant()
        node = 'BANANA'

        if len(self._string) > 1:
            left = self._string[:symbol[1]]
            right = self._string[symbol[1]+1:]
            # print(symbol, left, right)

            left = RegularExpression(left)._get_de_simone_tree()
            right = RegularExpression(right)._get_de_simone_tree()

            if symbol[0] == '|':
                node = DeSimoneAlternation(left,right)
            elif symbol[0] == '*':
                node = DeSimoneRepetition(left)
            elif symbol[0] == '.':
                node = DeSimoneConcatenation(left,right)
        else:
            node = DeSimoneNode(symbol[0])

        return node


    def to_deterministic_finite_automaton(self):
        pass

# "|" Alternation
# "*" Repetition
# "." Concatenation

class DeSimoneNode:
    def __init__(self, symbol, left=None, right=None):
        self._symbol = symbol
        self._left = left
        self._right = right

    def __str__(self):
        return '{%s[%s]%s}' % (self._left, self._symbol,self._right)

class DeSimoneAlternation(DeSimoneNode):
    def __init__(self, left, right):
        DeSimoneNode.__init__(self,'|',left,right)

class DeSimoneRepetition(DeSimoneNode):
    def __init__(self, left):
        DeSimoneNode.__init__(self,'*',left)

class DeSimoneConcatenation(DeSimoneNode):
    def __init__(self,left,right):
        DeSimoneNode.__init__(self,'.',left,right)

# a = RegularExpression('(ab)*|ba');
# print(a._get_de_simone_tree());
