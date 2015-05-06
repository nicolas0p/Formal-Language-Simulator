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
        automaton.insert_transition(q0, q1)

        self.assertTrue(automaton.has_transition(q0, q1))

#    def test_recognize_sentence(self):
#        q0 = State("q0")
#        q1 = State("q1")
#        states = {q0, q1}
#        transitions = {q0:q1, q1:q0}
#        automaton = DeterministicFiniteAutomaton(states, transitions, q0, {q1})
#        L(M) = odd sized sentences
#
#        automaton.recognize_sentence()
