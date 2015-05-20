import unittest
from deterministic_finite_automaton import DeterministicFiniteAutomaton
from deterministic_finite_automaton import State


class TestDeterministicFiniteAutomaton(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_automaton(self):
        automaton = DeterministicFiniteAutomaton(set(), {}, "", set())

        self.assertIsInstance(automaton, DeterministicFiniteAutomaton)

    def test_insert_state(self):
        automaton = DeterministicFiniteAutomaton(set(), {}, "", set())

        automaton.insert_state(State("q0"))

        self.assertEqual(1, automaton.state_quantity())

    def test_insert_transition(self):
        automaton = DeterministicFiniteAutomaton(set(), {'a'}, "", set())

        q0 = State("q0")
        q1 = State("q1")
        automaton.insert_state(q0)
        automaton.insert_state(q1)
        automaton.insert_transition(q0, 'a', q1)

        self.assertTrue(automaton.has_transition(q0, 'a', q1))

    def test_insert_false_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton({q0}, alphabet, q0, {q0})

        self.assertRaises(Exception, automaton.insert_transition, q0, 'c', q0)
        self.assertRaises(Exception, automaton.insert_transition, q0, 'a', q1)

    def test_recognize_true_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)
        #L(M) = odd sized sentences

        self.assertTrue(automaton.recognize_sentence("aba"))

    def test_dont_recognize_false_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)
        #L(M) = odd sized sentences

        self.assertFalse(automaton.recognize_sentence("abaa"))
        self.assertFalse(automaton.recognize_sentence("abc"))

    def test_remove_state(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        states = {q0, q1, q2}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q2)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q2)
        automaton.insert_transition(q2, 'a', q0)
        automaton.insert_transition(q2, 'a', q1)

        automaton.remove_state(q1)

        self.assertFalse(automaton.has_transition(q0, 'a', q1))
        self.assertFalse(automaton.has_transition(q1, 'a', q0))
        self.assertTrue(automaton.has_transition(q0, 'b', q2))
        self.assertSetEqual(automaton._states, {q0, q2})

    def test_remove_unreachable_states(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)

        automaton.remove_unreachable_states()

        self.assertSetEqual(automaton._states, {q0,q1})

    def test_remove_dead_states(self):
        q = []
        for i in range(0,6):
            q.append(State("q" + str(i)))
        states = set(q)
        alphabet = {'a','b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q[0], {q[2]})
        automaton.insert_transition(q[0], 'a', q[1])
        automaton.insert_transition(q[0], 'b', q[3])
        automaton.insert_transition(q[1], 'a', q[2])
        automaton.insert_transition(q[1], 'b', q[2])
        automaton.insert_transition(q[3], 'a', q[5])
        automaton.insert_transition(q[4], 'a', q[3])
        automaton.insert_transition(q[5], 'a', q[4])

        automaton.remove_dead_states()

        self.assertSetEqual(automaton._states, {q[0], q[1], q[2]})
'''
    TEST DISABLES UNTIL EQUALS BETWEEN DFA IS IMPLEMENTED
    def test_remove_equivalent_states(self):
        q = []
        for i in range(0,6):
            q.append(State("q" + str(i)))
        states = set(q)
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, q[0], {q[0], q[5]})
        automaton.insert_transition(q[0], 'a', q[5])
        automaton.insert_transition(q[0], 'b', q[1])
        automaton.insert_transition(q[1], 'a', q[4])
        automaton.insert_transition(q[1], 'b', q[3])
        automaton.insert_transition(q[2], 'a', q[2])
        automaton.insert_transition(q[2], 'b', q[5])
        automaton.insert_transition(q[3], 'a', q[4])
        automaton.insert_transition(q[3], 'b', q[0])
        automaton.insert_transition(q[4], 'a', q[1])
        automaton.insert_transition(q[4], 'b', q[2])
        automaton.insert_transition(q[5], 'a', q[5])
        automaton.insert_transition(q[5], 'b', q[4])

        old = copy.deepcopy(automaton)
        automaton.remove_equivalent_states()

        self.assertTrue(automaton == old)
'''
