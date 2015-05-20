import unittest
from finite_automaton import FiniteAutomaton
from finite_automaton import State


class TestFiniteAutomaton(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_automaton(self):
        automaton = FiniteAutomaton(set(), {}, "", set())

        self.assertIsInstance(automaton, FiniteAutomaton)

    def test_insert_state(self):
        automaton = FiniteAutomaton(set(), {}, "", set())

        automaton.insert_state(State("q0"))

        self.assertEqual(1, automaton.state_quantity())

    def test_insert_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        automaton = FiniteAutomaton({q0, q1}, {'a'}, "", set())

        automaton.insert_transition(q0, 'a', q1)

        self.assertTrue(automaton.has_transition(q0, 'a', q1))

    def test_insert_false_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton({q0}, alphabet, q0, {q0})

        self.assertRaises(Exception, automaton.insert_transition, q0, 'c', q0)
        self.assertRaises(Exception, automaton.insert_transition, q0, 'a', q1)

    def test_recognize_true_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)
        #L(M) = odd sized sentences

        self.assertFalse(automaton.is_nondeterministic())
        self.assertTrue(automaton.recognize_sentence("aba"))

    def test_dont_recognize_false_sentence(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)
        #L(M) = odd sized sentences

        self.assertFalse(automaton.is_nondeterministic())
        self.assertFalse(automaton.recognize_sentence("abaa"))
        self.assertFalse(automaton.recognize_sentence("abc"))

    def test_remove_state(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        states = {q0, q1, q2}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q1})
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
        automaton = FiniteAutomaton(states, alphabet, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)

        automaton.remove_unreachable_states()

        self.assertSetEqual(automaton._states, {q0,q1})

    def test_remove_dead_states(self):
        q = []
        for i in range(0,6):
            q.append(State("q" + str(i)))
        states = set(q)
        alphabet = {'a','b'}
        automaton = FiniteAutomaton(states, alphabet, q[0], {q[2]})
        automaton.insert_transition(q[0], 'a', q[1])
        automaton.insert_transition(q[0], 'b', q[3])
        automaton.insert_transition(q[1], 'a', q[2])
        automaton.insert_transition(q[1], 'b', q[2])
        automaton.insert_transition(q[3], 'a', q[5])
        automaton.insert_transition(q[4], 'a', q[3])
        automaton.insert_transition(q[5], 'a', q[4])

        automaton.remove_dead_states()

        self.assertSetEqual(automaton._states, {q[0], q[1], q[2]})

    def test_add_nondeterministic_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        automaton = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q1})
        automaton.insert_transition(q0, 'a', q0)
        automaton.insert_transition(q1, 'b', q1)

        automaton.insert_transition(q0, 'a', q1)

        self.assertTrue(automaton.is_nondeterministic())
        self.assertTrue(automaton.has_transition(q0, 'a', q0))
        self.assertTrue(automaton.has_transition(q0, 'a', q1))

    def test_automata_union(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton1 = FiniteAutomaton(states, alphabet, q0, {q1})
        automaton1.insert_transition(q0, 'a', q1)
        automaton1.insert_transition(q0, 'b', q1)
        automaton1.insert_transition(q1, 'a', q0)
        automaton1.insert_transition(q1, 'b', q0)
        #L(M) = {x|x in (a,b)* ^ |x| is odd}
        s0 = State("q0")
        s1 = State("q1")
        states = {s0, s1}
        alphabet = {'a', 'b'}
        automaton2 = FiniteAutomaton(states, alphabet, s0, {s0})
        automaton2.insert_transition(s0, 'a', s1)
        automaton2.insert_transition(s0, 'b', s1)
        automaton2.insert_transition(s1, 'a', s0)
        automaton2.insert_transition(s1, 'b', s0)
        #L(M) = {x|x in (a,b)* ^ |x| is even}

        union = automaton1.union(automaton2)

        self.assertTrue(automaton1.recognize_sentence("abaab"))
        self.assertTrue(automaton2.recognize_sentence("ababba"))
        self.assertFalse(automaton1.recognize_sentence("ababba"))
        self.assertFalse(automaton2.recognize_sentence("abaab"))
        self.assertTrue(union.recognize_sentence("abaab"))
        self.assertTrue(union.recognize_sentence("ababba"))
        self.assertFalse(union.recognize_sentence("abc"))
