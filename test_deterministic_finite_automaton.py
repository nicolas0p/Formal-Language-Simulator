import unittest
from deterministic_finite_automaton import DeterministicFiniteAutomaton
from deterministic_finite_automaton import State


class TestDeterministicFiniteAutomaton(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_automaton(self):
        automaton = DeterministicFiniteAutomaton(set(), set(), {}, "", set())

        self.assertIsInstance(automaton, DeterministicFiniteAutomaton)

    def test_insert_state(self):
        automaton = DeterministicFiniteAutomaton(set(), set(), {}, "", set())

        automaton.insert_state(State("q0"))

        self.assertEqual(1, automaton.state_quantity())

    def test_insert_transition(self):
        automaton = DeterministicFiniteAutomaton(set(), set(), {}, "", set())

        q0 = State("q0")
        q1 = State("q1")
        automaton.insert_state(q0)
        automaton.insert_state(q1)
        automaton.insert_transition(q0, 'a', q1)

        self.assertTrue(automaton.has_transition(q0, 'a', q1))

    def test_recognize_true_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        transitions = {q0:{'a':q1, 'b':q1}, q1:{'a':q0, 'b':q0}}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, transitions, q0, {q1})
        #L(M) = odd sized sentences

        self.assertTrue(automaton.recognize_sentence("aba"))

    def test_dont_recognize_false_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        transitions = {q0:{'a':q1, 'b':q1}, q1:{'a':q0, 'b':q0}}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, transitions, q0, {q1})
        #L(M) = odd sized sentences

        self.assertFalse(automaton.recognize_sentence("abaa"))
        self.assertFalse(automaton.recognize_sentence("abc"))

    def test_remove_state(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        states = {q0, q1, q2}
        transitions = {q0:{'a':q1, 'b':q2}, q1:{'a':q0, 'b':q2}, q2:{'a':q0, 'b':q1}}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, transitions, q0, {q1})

        automaton.remove_state(q1)

        self.maxDiff = None
        self.assertDictEqual(automaton._transitions, {q0:{'b':q2}, q2:{'a':q0}})
        self.assertSetEqual(automaton._states, {q0, q2})

    def test_remove_unreachable_states(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        states = {q0, q1}
        transitions = {q0:{'a':q1}, q1:{}, q2:{}}
        alphabet = {'a', 'b'}
        automaton = DeterministicFiniteAutomaton(states, alphabet, transitions, q0, {q1})

        automaton.remove_unreachable()

        self.assertSetEqual(automaton._states, {q0,q1})
