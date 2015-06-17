import copy
import string
"""
@package Pacote contém autômato finito e estados
"""

class FiniteAutomaton():
    """Classe que representa o autômato finito, determinístico ou não
    """

    def __init__(self, states, alphabet, initial_state, final_states):
        """Construtor de autômato finito
        @param states Conjunto de estados do autômato
        @param alphabet Conjunto de caracteres
        @param initial_state Estado inicial
        @param final_states Conjunto de estados finais
        @throws Exception Se algum membro do alfabeto tem tamanho diferente de um
        """
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
        """Insere estado
        @param state Estado a ser adicionado
        """
        self._states.add(state)
        self._transitions[state] = {}
        for letter in self._alphabet:
            self._transitions[state][letter] = set()

    def rename_states(self):
        """Adequa o nome dos estados ao requisito.
        O requisito é que o nome de cada estado seja uma letra maiúscula
        """
        states = list(self._states)
        for i in range(0, len(self._states)):
            self._change_state_name(states[i], self._generate_name(i))

    def _generate_name(self, number):
        alphabet = list(string.ascii_uppercase)
        result = []
        result.insert(1, alphabet[number % 26])
        if number > 26:
            position = number // 26
            result.insert(0, alphabet[position])
        return ''.join(result)

    def state_quantity(self):
        """Retorna a quantidade de estados
        @return A quantidade de estados
        """
        return len(self._states)

    def is_nondeterministic(self):
        """Retorna se o autômato é não determinístico
        """
        for state in self._states:
            has_epsilon = self._transitions[state][self._epsilon] != set()
            for letter in self._alphabet:
                if len(self._transitions[state][letter]) > 1:
                    return True
                if has_epsilon and len(self._transitions[state][letter]) > 0:
                    return True
        return False

    def insert_transition(self, source, letter, destiny):
        """Insere uma transição no autômato
        @param source Estado de onde a transição parte
        @param letter Letra pela qual a transição vai ocorrer
        @param destiny Estado para onde a transição chega
        @throws Exception Se algum dos estados não pertence ao conjunto de estados
        @throws Exception Se a letra não pertence ao alfabeto
        """
        if source not in self._states or destiny not in self._states:
            raise Exception("State does not belong to finite automaton")
        if letter not in self._alphabet:
            raise Exception("Letter does not belong to alphabet")
        self._transitions[source][letter].add(destiny)

    def remove_transition(self, source, letter, destiny):
        """Remove uma transição do autômato.
        Se a transição não existe, nada é feito
        @param source Estado de onde a transição a ser retirada parte
        @param letter Letra por onde a transição a ser retirada ocorre
        @param destiny Estado para onde a transição a ser retirada chega
        """
        try:
            self._transitions[source][letter].remove(destiny)
        except KeyError:
            return

    def has_transition(self, source, letter, destiny):
        """Retorna se a transição indicada existe
        @param source Estado de onde a transição parte
        @param letter Letra pela qual a transição ocorre
        @param destiny Estado para onde a transição chega
        @return Se a transição existe
        """
        try:
            return destiny in self._transitions[source][letter]
        except KeyError:
            return False

    def recognize_sentence(self, sentence):
        """Faz o reconhecimento, ou não, da sentença
        @param sentence Sentença a ser testada
        @return Se a sentença é reconhecida ou não pelo autômato
        """
        return self._recognize_sentence(sentence, self._initial_state)

    def _recognize_sentence(self, sentence, actual_state):
        """Método recursivo de reconhecimento de sentença.
        Representa o estado que o autômato está e o fragmento de sentença que ele ainda não reconheceu
        @param sentence Sequência de caracteres a ser testada
        @param actual_state Estado atual do reconhecimento
        """
        if sentence is "":
            return actual_state in self._final_states
        if sentence[0] not in self._alphabet:
            return False
        through_epsilon = self._transitions[actual_state][self._epsilon]
        for state in self._transitions[actual_state][sentence[0]]:
            if self._recognize_sentence(sentence[1:], state):
                return True
        for state in through_epsilon:
            if self._recognize_sentence(sentence, state):
                return True
        return False

    def remove_unreachable_states(self):
        """Remove estados inalcançáveis
        """
        reachable = self.find_reachable()
        for state in self._states - reachable:
            self.remove_state(state)

    def remove_state(self, remove_state):
        """Remove um estado do autômato.
        Remove também as transições que partem e que chegam neste estado
        @param remove_state Estado a ser removido
        """
        for state in self._states:
            transitions = self._transitions[state].copy()
            for letter in transitions:
                if remove_state in self._transitions[state][letter]:
                    self._transitions[state][letter].remove(remove_state)
        del self._transitions[remove_state]
        self._states.remove(remove_state)

    def find_reachable(self):
        """Gera um conjunto com os estados alcançáveis
        @return Conjunto de estados alcançáveis
        """
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
            reachable_state.update(temp)
        return reachable_state

    def remove_dead_states(self):
        """Remove estados mortos
        """
        dead = self._find_dead_states()
        for state in dead:
            self.remove_state(state)

    def _find_dead_states(self):
        """Gera o conjunto de estados mortos
        @return Conjunto de estados mortos
        """
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
        """União de autômatos
        @param other Autômato que se deseja unir
        @return Autômato que representa a união do autômato atual com other
        """
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
        """Faz o complemento do autômato.
        Se o autômato for não determinístico, ele é determinizado antes de se fazer o complemento
        @return O complemente do autômato atual
        """
        automaton = self.copy()
        automaton.determinize()
        automaton._add_error_state()
        new_final_states = automaton._states - automaton._final_states
        automaton._final_states = new_final_states
        return automaton

    def _add_error_state(self):
        """Adiciona o estado de erro se o autômato contém transições não definidas
        @return O estado de erro, se ele foi adicionado
        """
        if self.is_completely_defined():
            return
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
        """Interseção de autômatos
        @return O autômato que representa a interseção entre o autômato atual com other
        """
        complement1 = self.complement()
        complement2 = other.complement()
        union = complement1.union(complement2)
        final = union.complement()
        return final

    def _epsilon_closure(self, state):
        """Gera o epsilon fecho de um dado estado
        @param state Estado que se deseja obter o epsilon fecho
        @return conjunto de estados no epsilon fecho do estado
        """
        closure = {state}
        old = set()
        while old != closure:
            old = closure.copy()
            for q in old:
                closure.update(self._transitions[q][self._epsilon])
        return closure

    def determinize(self):
        """Determinização e remoção de epsilon transições de autômato
        """
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
                for letter in self._alphabet - {self._epsilon}:
                    destiny_union = set()
                    for state in multi_state:
                        closure = self._epsilon_closure(state)
                        for q in closure:
                            pluri_destiny = self._transitions[q][letter]
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
                if destiny_union == set():
                    transitions[new_state][letter] = set()

        self._states = states
        self._final_states = final_states
        self._transitions = transitions

    def is_empty(self):
        """Detecta se a linguagem reconhecida pelo autômato é a linguagem vazia
        @return Se a linguagem reconhecida pelo autômato é a linguagem vazia
        """
        return self._initial_state not in (self._states - self._find_dead_states())

    def copy(self):
        """Faz uma cópia de autômato
        @return cópia do autômato atual
        """
        automaton = FiniteAutomaton(self._states.copy(), self._alphabet.copy(), self._initial_state.copy(), self._final_states.copy())
        automaton._transitions = copy.deepcopy(self._transitions)
        return automaton

    def __repr__(self):
        """Gera uma representação imprimível do autômato
        @return String que representa o autômato
        """
        alp = str(self._alphabet)
        states = str(self._states)
        trans = str(self._transitions)
        initial = str(self._initial_state)
        finals = str(self._final_states)
        return str(alp + states + trans + initial + finals)

    def remove_equivalent_states(self):
        """Remove os estados equivalentes
        """
        if self._states == set():
            return
        self.determinize()
        self._add_error_state()
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
        initial_state_class_nb = [equivalence_classes.index(y) for y in equivalence_classes if self._initial_state in y][0]
        self._initial_state = q[initial_state_class_nb]
        self._states = set(q)
        self._transitions = transitions
        self._final_states = final_states
        self.remove_dead_states()

    def _find_equivalence_classes(self):
        """Encontra as classes de equivalência
        @return Lista de conjuntos de estados, cada um desses conjuntos contêm estados equivalentes
        """
        equivalence_classes = [self._final_states.copy(), self._states - self._final_states]
        old = []
        while equivalence_classes != old:
            old = copy.deepcopy(equivalence_classes)
            equivalence_classes = []
            for clas in old:
                equivalence_classes.extend(self._find_equivalent_states(clas, old))
        return equivalence_classes

    def _find_equivalent_states(self, clas, old):
        """Gera dois (ou um) conjunto de estados a partir de uma classe da iteração anterior.
        Uma das classes representa os estados da classe anterior que são equivalentes, e a outra representa os estados que não são equivalentes com os estados do outro conjunto
        @param clas Conjunto de estados que representa a classe de equivalencia a ser analisada
        @param old Lista dos conjuntos que representam as classes de equivalência da iteração anterior
        """
        equivalence_classes = []
        state1 = next(iter(clas))
        not_equal = set()
        equal = {state1}
        for state2 in clas:
            if not self._are_equivalent_states(state1, state2, old):
                not_equal.add(state2)
            else:
                equal.add(state2)
        equivalence_classes.append(equal)
        if len(not_equal) > 1:
            equivalence_classes.extend(self._find_equivalent_states(not_equal, old))
        elif len(not_equal) == 1:
            equivalence_classes.append(not_equal)
        return equivalence_classes

    def _are_equivalent_states(self, state1, state2, equivalence_classes):
        """Determina se dois estados são equivalentes ou não
        @param state1 Estado a ser comparado
        @param state2 Outro estado a ser comparado
        @param equivalence_classes Lista de conjuntos que representa as classes de equivalência da iteração anterior
        @return Se state 1 é equivalente a state2
        """
        for letter in self._alphabet - {self._epsilon}:
            tran_state1 = next(iter(self._transitions[state1][letter]))
            tran_state2 = next(iter(self._transitions[state2][letter]))
            one = [x for x in equivalence_classes if tran_state1 in x][0]
            if tran_state2 not in one:
                return False
        return True

    def is_completely_defined(self):
        """Determina se o autômato atual é completamente definido,ou seja, se não possui transições não definidas
        @return Se o autômato é completamente definido
        """
        for letter in self._alphabet - {self._epsilon}:
            for state in self._states:
                if self._transitions[state][letter] == set():
                    return False
        return True

    def minimize(self):
        """Minimiza o autômato atual
        """
        self.determinize()
        self.remove_unreachable_states()
        self.remove_dead_states()
        self.remove_equivalent_states()

    def __sub__(self, other):
        """Subtrai dois autômatos
        @param other Autômato que vai subtrair o autômato atual
        """
        return self.intersection(other.complement())

    def is_equal(self, other):
        """Determina se dois autômatos são equivalentes, ou seja, se eles reconhecem linguagens iguais
        @param other Autômato a ser comparado com o atual
        """
        return (self - other).is_empty() and (other - self).is_empty()

    def _change_state_name(self, target, new_name):
        """Muda o nome de um estado, atualizando todas as transições
        @param target Estado que terá seu nome mudado
        @param new_name Novo nome do estado target
        """
        self._states.remove(target)
        new_state = State(new_name)
        self._states.add(new_state)
        self._transitions[new_state] = self._transitions[target]
        del self._transitions[target]
        for state in self._states:
            for letter in self._alphabet:
                through_transitions = self._transitions[state][letter]
                if target in through_transitions:
                    through_transitions.remove(target)
                    through_transitions.add(new_state)
        if target in self._final_states:
            self._final_states.remove(target)
            self._final_states.add(new_state)
        if self._initial_state == target:
            self._initial_state = new_state

class State():
    """Classe que representa um estado de um autômato finito
    """

    def __init__(self, name):
        """Construtor de estado
        @param name Nome do estado
        """
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def copy(self):
        return State(self._name)

    def __eq__(self, other):
        """Comparador de estados, se dois estados tem o mesmo nome, eles são o mesmo estado
        @param other Outro estado a ser comparado
        """
        return self._name == other._name

    def __lt__(self, other):
        return self._name < other._name

    def __repr__(self):
        return self._name
