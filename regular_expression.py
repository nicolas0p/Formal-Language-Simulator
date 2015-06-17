from finite_automaton import FiniteAutomaton
from finite_automaton import State

class RegularExpression:
    def __init__(self, string):
        self._string = string
        self._terminals = {symbol for symbol in string if symbol not in "()|+?.*"}
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
                ( pair[0] == '?' and pair[1] in self._terminals ) or \
                ( pair[0] == '*' and pair[1] == '(' ) or \
                ( pair[0] == '?' and pair[1] == '(' ) or \
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
                elif char == '?' and less_significant[0] not in ['|','.','*','?']:
                    less_significant = ('?',i)
                elif less_significant[0] not in ['|','.','*','?']:
                    less_significant = (char,i)

        return less_significant

    def _get_de_simone_tree(self):
        symbol = self._get_less_significant()
        node = None

        if len(self._string) > 1:
            left = self._string[:symbol[1]]
            right = self._string[symbol[1]+1:]

            left = RegularExpression(left)._get_de_simone_tree()
            right = RegularExpression(right)._get_de_simone_tree()

            if symbol[0] == '|':
                node = DeSimoneAlternation(left,right)
            elif symbol[0] == '*':
                node = DeSimoneRepetition(left)
            elif symbol[0] == '?':
                node = DeSimoneOption(left)
            elif symbol[0] == '.':
                node = DeSimoneConcatenation(left,right)

            left._parent = node
            right._parent = node
        else:
            node = DeSimoneNode(symbol[0])

        return node


    def to_deterministic_finite_automaton(self):
        tree = self._get_de_simone_tree()

        # creating the initial state of the automaton, as it should have at least one state
        initial_state = State('q0')
        # gonna use this to create generic names for the states, as "q1","q2","q3"
        state_numerator = 1;

        # will be the table we have the states layed out, as if we were doing it by hand
        table = []
        # we put the first state and its composition, so we're ready to start the loop by analyzing its composition
        # and take the information needed to create the other states
        table.append({'state':initial_state, 'transitions':{}, 'composition':tree.down(), 'final': False})
        # the other states are put after the initial one on the table, so the loop doesnt end until it analyzes all
        # the needed states

        for state in table:

            # we're looping through the states already on the table, these are the states we're certain will be needed
            # we'll be analyzing their composition and decide if a new state is needed

            for node in state['composition']:
                ### print(state['state'], node)

                # looking at each node on the composition of a state,
                # if we find lambda this state is final, so we mark it as so
                if node._symbol == 'Lambda':
                    state['final'] = True
                # if it's not lambda, and there isn't a transition through this state symbol
                # we create this transition, and put a supposed new state there
                # we also populate this new state composition with the node thread back
                # se we can after this decide if a new state is needed on the table, or we can use a state with the
                # same composition that is already on the table
                elif node._symbol not in state['transitions']:
                    new_state = State('q%i' % state_numerator)
                    state_numerator += 1
                    state['transitions'][node._symbol] = {'state':new_state,'composition':node._thread_back().up()}
                # and if we already have a transition through this node symbol we then unite this node's thread back
                # with the supposed new state composition
                else:
                    state['transitions'][node._symbol]['composition'] |= node._thread_back().up()

            # at this point we have supposed new states on this state transitions
            # we need to analyze if their compositions aren't identical to a state's composition already on the table
            # if this happen, we replace the supposed new state with the one on the table
            # otherwise, if there isn't a state with its composition on the table, we put the new state on it

            for transition_symbol in state['transitions']:
                new_state = state['transitions'][transition_symbol]
                # if this state composition is not identical to any state's on table composition
                # then we add this state to the table
                if new_state['composition'] not in [line['composition'] for line in table]:
                    table.append({'state':new_state['state'],'transitions':{}, 'composition': new_state['composition'], 'final': False})
                # if we already have a state with this state's composition on the table
                # then we replace this state on the transition by the one that is already on the table
                else:
                    # what a beatiful line of code, sqn
                    state['transitions'][transition_symbol] = [line for line in table if line['composition'] == new_state['composition']][0]

        # now we have all the states on the table and they're linked to each other througt the transitions
        # they're already marked as final if they're so
        # so we'll begin to mount the automaton, FiniteAutomaton(states, alphabet, initial_state, final_states)

        states = set([line['state'] for line in table])

        # could be replaced by the terminals found on the transitions
        alphabet = self._terminals

        # initial_state is already setted

        final_states = set([line['state'] for line in table if line['final']])

        fa = FiniteAutomaton(states, alphabet, initial_state, final_states)

        # now we need to add the transitions
        for state in table:
            for transition_symbol in state['transitions']:
                fa.insert_transition(state['state'], transition_symbol, state['transitions'][transition_symbol]['state'])

        # supposedly should already be deterministic

        return fa

# "|" Alternation
# "*" Repetition
# "." Concatenation

class DeSimoneNode:
    def __init__(self, symbol, left=None, right=None):
        self._symbol = symbol
        self._left = left
        self._right = right
        self._parent = None

    def __str__(self):
        return '{%s[%s]%s}' % (self._left, self._symbol,self._right)

    def down(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        return {self}

    def _thread_back(self):
        if self._parent == None:
            return DeSimoneLambda
        elif self._parent._left == self:
            return self._parent
        else:
            return self._parent._thread_back()

class DeSimoneLambda:
    _symbol = 'Lambda'
    def up(seenUp = set(),seenDown = set()):
        return {DeSimoneLambda}

class DeSimoneAlternation(DeSimoneNode):
    def __init__(self, left, right):
        DeSimoneNode.__init__(self,'|',left,right)

    def down(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenDown):
            seenDown |= {self}
            return self._left.down(seenUp, seenDown) | self._right.down(seenUp, seenDown)
        else:
            return set()

    def up(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenUp):
            seenUp |= {self}
            return self._thread_back().up(seenUp,seenDown)
        else:
            return set()

class DeSimoneRepetition(DeSimoneNode):
    def __init__(self, left):
        DeSimoneNode.__init__(self,'*',left)

    def down(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenDown):
            seenDown |= {self}
            return self._left.down(seenUp,seenDown) | self._thread_back().up(seenUp,seenDown)
        else:
            return set()

    def up(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenUp):
            seenUp |= {self}
            return self._left.down(seenUp,seenDown) | self._thread_back().up(seenUp,seenDown)
        else:
            return set()

class DeSimoneOption(DeSimoneNode):
    def __init__(self, left):
        DeSimoneNode.__init__(self,'?',left)

    def down(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenDown):
            seenDown |= {self}
            return self._left.down(seenUp, seenDown) | self._thread_back().up(seenUp, seenDown)
        else:
            return set()

    def up(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenUp):
            seenUp |= {self}
            return self._thread_back().up(seenUp, seenDown)
        else:
            return set()

class DeSimoneConcatenation(DeSimoneNode):
    def __init__(self,left,right):
        DeSimoneNode.__init__(self,'.',left,right)

    def down(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenDown):
            seenDown |= {self}
            return self._left.down(seenUp, seenDown)
        else:
            return set()

    def up(self,seenUp = None,seenDown = None):
        if seenUp is None:
            seenUp = set()
        if seenDown is None:
            seenDown = set()

        if(self not in seenUp):
            seenUp |= {self}
            return self._right.down(seenUp, seenDown)
        else:
            return set()
