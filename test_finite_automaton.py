import unittest
from finite_automaton import FiniteAutomaton
from finite_automaton import State

import pdb

class TestFiniteAutomaton(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_automaton(self):
        automaton = FiniteAutomaton(set(), set(), State(""), set())

        self.assertIsInstance(automaton, FiniteAutomaton)

    def test_insert_state(self):
        automaton = FiniteAutomaton(set(), set(), State(""), set())

        automaton.insert_state(State("q0"))

        self.assertEqual(1, automaton.state_quantity())

    def test_insert_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        automaton = FiniteAutomaton({q0, q1}, {'a'}, q0, set())

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
        for i in range(0, 6):
            q.append(State("q" + str(i)))
        states = set(q)
        alphabet = {'a', 'b'}
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
        s0 = State("s0")
        s1 = State("s1")
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

    def test_automata_union_2(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q0, q1})
        automaton.insert_transition(q0, 'a', q0)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        #L(M) = {x|x in (a,b)* ^ bb not in x}
        q2 = State("q2")
        other = FiniteAutomaton({q0, q1, q2}, alphabet, q0, {q0, q1, q2})
        other.insert_transition(q0, 'a', q0)
        other.insert_transition(q0, 'b', q1)
        other.insert_transition(q1, 'a', q0)
        other.insert_transition(q1, 'b', q2)
        other.insert_transition(q2, 'a', q0)
        #L(M) = {x|x in (a,b)* ^ bbb not in x}

        union = automaton.union(other)

        self.assertTrue(union.recognize_sentence("baababa"))
        self.assertFalse(union.recognize_sentence("aaababbbaaba"))

    def test_automata_union_3(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q0, q1})
        automaton.insert_transition(q0, 'a', q0)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        #L(M) = {x|x in (a,b)* ^ bb not in x}
        q2 = State("q2")
        div3 = FiniteAutomaton({q0, q1, q2}, {'a', 'b'}, q0, {q0})
        div3.insert_transition(q0, 'a', q1)
        div3.insert_transition(q0, 'b', q1)
        div3.insert_transition(q1, 'a', q2)
        div3.insert_transition(q1, 'b', q2)
        div3.insert_transition(q2, 'a', q0)
        div3.insert_transition(q2, 'b', q0)

        union = automaton.union(div3)

        self.assertTrue(union.recognize_sentence("abbaaabba"))
        self.assertTrue(union.recognize_sentence("aaabaaabaa"))
        self.assertFalse(union.recognize_sentence("bbabbaa"))


    def test_recognize_nondeterministic(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q3})
        automaton.insert_transition(q0, 'a', q0)
        automaton.insert_transition(q0, 'b', q0)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q2)
        automaton.insert_transition(q2, 'b', q3)
        automaton.insert_transition(q3, 'a', q3)
        automaton.insert_transition(q3, 'b', q3)

        self.assertTrue(automaton.recognize_sentence("abaababaaaba"))
        self.assertFalse(automaton.recognize_sentence("aaaabaaab"))

    def test_automaton_complement(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton({q0, q1, q2}, alphabet, q0, {q0})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q0)
        automaton.insert_transition(q1, 'b', q1)
        automaton.insert_transition(q1, 'a', q2)
        automaton.insert_transition(q2, 'b', q2)
        automaton.insert_transition(q2, 'a', q0)
        #L(M) = {x | x in (a,b)* ^ #a's is divisible by 3}

        complement = automaton.complement()

        self.assertTrue(automaton.recognize_sentence("baabbababaabb"))
        self.assertFalse(automaton.recognize_sentence("abbabababbba"))
        self.assertTrue(complement.recognize_sentence("abbabababbba"))
        self.assertFalse(complement.recognize_sentence("baabbababaabb"))

    def test_determinize_automaton(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q3})
        automaton.insert_transition(q0, 'a', q0)
        automaton.insert_transition(q0, 'b', q0)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q2)
        automaton.insert_transition(q2, 'b', q3)
        automaton.insert_transition(q3, 'a', q3)
        automaton.insert_transition(q3, 'b', q3)
        #{x|x in (a,b)* and bab in x}
        determinized = automaton.copy()

        determinized.determinize()

        self.assertTrue(automaton.is_nondeterministic())
        self.assertFalse(determinized.is_nondeterministic())
        self.assertTrue(determinized.recognize_sentence("abaaababbbaaaab"))
        self.assertTrue(determinized.recognize_sentence("baaaaaabbbbbbbbabbaaaaaa"))
        self.assertFalse(determinized.recognize_sentence("aaaabaabaabaabaab"))

    def test_automaton_intersection(self):
        q0 = State("q0")
        q1 = State("q1")
        states = {q0, q1}
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q0, {q0})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)
        #L(M) = {x|x in (a,b)* ^ |x| is even}
        other = FiniteAutomaton(states, alphabet, q0, {q0, q1})
        other.insert_transition(q0, 'a', q0)
        other.insert_transition(q0, 'b', q1)
        other.insert_transition(q1, 'a', q0)
        #L(M) = {x|x in (a,b)* ^ bb not in x}

        intersection = automaton.intersection(other)

        self.assertTrue(automaton.recognize_sentence("aabaab"))
        self.assertTrue(other.recognize_sentence("aabaab"))
        self.assertTrue(intersection.recognize_sentence("aabaab"))
        self.assertFalse(intersection.recognize_sentence("abbaaa"))

    def test_remove_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        automaton = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q0, 'b', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, 'b', q0)

        automaton.remove_transition(q0, 'a', q1)

        self.assertFalse(automaton.has_transition(q0, 'a', q1))
        self.assertTrue(automaton.has_transition(q0, 'b', q1))
        self.assertTrue(automaton.has_transition(q1, 'a', q0))

    def test_all_alphabet_members_are_one_character_only(self):
        q0 = State("q0")
        self.assertRaises(Exception, FiniteAutomaton, {q0}, {'b', 'ab'}, q0, {q0})

    def test_is_the_empty_language(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q3})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'b', q2)
        automaton.insert_transition(q3, 'a', q2)

        self.assertTrue(automaton.is_empty())

    def test_is_not_the_empty_language(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q3})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'b', q2)
        automaton.insert_transition(q2, 'a', q3)
        automaton.insert_transition(q3, 'a', q2)

        self.assertFalse(automaton.is_empty())

    def test_remove_equivalent_states(self):
        q = []
        for i in range(0, 6):
            q.append(State("q" + str(i)))
        states = set(q)
        alphabet = {'a', 'b'}
        automaton = FiniteAutomaton(states, alphabet, q[0], {q[0], q[5]})
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
        old = automaton.copy()

        automaton.remove_equivalent_states()

        self.assertTrue(old.recognize_sentence("aaaaaaababba"))
        self.assertTrue(automaton.recognize_sentence("aaaaaaababba"))
        self.assertFalse(old.recognize_sentence("baaaaba"))
        self.assertFalse(automaton.recognize_sentence("baaaaba"))

    def test_is_automata_completely_defined(self):
        q0 = State("q0")
        q1 = State("q1")
        automaton = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q1})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'a', q0)

        self.assertFalse(automaton.is_completely_defined())

    def test_minimize_automaton(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q0, q2})
        automaton.insert_transition(q0, 'b', q2)
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'b', q1)
        automaton.insert_transition(q1, 'a', q2)
        automaton.insert_transition(q2, 'b', q2)
        automaton.insert_transition(q2, 'a', q3)
        automaton.insert_transition(q3, 'b', q3)
        automaton.insert_transition(q3, 'a', q2)

        automaton.minimize()

        self.assertSetEqual(automaton._states, {q0, q1})
        self.assertTrue(automaton.recognize_sentence("baabaabaababab"))

    def test_automata_subtraction(self):
        q0 = State("q0")
        q1 = State("q1")
        abstar = FiniteAutomaton({q0}, {'a', 'b'}, q0, {q0})
        abstar.insert_transition(q0, 'a', q0)
        abstar.insert_transition(q0, 'b', q0)

        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)

        subtraction = abstar - evena

        self.assertTrue(subtraction.recognize_sentence("babbbaba"))
        self.assertTrue(subtraction.recognize_sentence("a"))
        self.assertFalse(subtraction.recognize_sentence("abababa"))

    def test_automata_equality(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        q3 = State("q3")
        automaton = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q0, q2})
        automaton.insert_transition(q0, 'b', q2)
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'b', q1)
        automaton.insert_transition(q1, 'a', q2)
        automaton.insert_transition(q2, 'b', q2)
        automaton.insert_transition(q2, 'a', q3)
        automaton.insert_transition(q3, 'b', q3)
        automaton.insert_transition(q3, 'a', q2)

        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)

        self.assertTrue(evena.is_equal(automaton))

    def test_recognize_sentence_with_epsilon_transition(self):
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        automaton = FiniteAutomaton({q0, q1, q2}, {'a', 'b'}, q0, {q2})
        automaton.insert_transition(q0, 'a', q1)
        automaton.insert_transition(q1, 'a', q0)
        automaton.insert_transition(q1, '&', q2)
        automaton.insert_transition(q2, 'b', q2)

        self.assertTrue(automaton.recognize_sentence("aaab"))
        self.assertTrue(automaton.recognize_sentence("aaaaabbbbbbbb"))
        self.assertFalse(automaton.recognize_sentence("aaaabbb"))

    def test_change_state_name(self):
        q0 = State("q0")
        q1 = State("q1")
        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)

        evena._change_state_name(q0, "q2")

        self.assertTrue(evena.recognize_sentence("bbabaabba"))
        self.assertTrue(evena.recognize_sentence("aaaa"))
        self.assertFalse(evena.recognize_sentence("abbabaabbab"))

    def test_equality_2(self):
        q0 = State("q0")
        q1 = State("q1")
        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)
        q2 = State("q2")
        q3 = State("q3")
        amod4 = FiniteAutomaton({q0, q1, q2, q3}, {'a', 'b'}, q0, {q0})
        amod4.insert_transition(q0, 'b', q0)
        amod4.insert_transition(q0, 'a', q1)
        amod4.insert_transition(q1, 'b', q1)
        amod4.insert_transition(q1, 'a', q2)
        amod4.insert_transition(q2, 'b', q2)
        amod4.insert_transition(q2, 'a', q3)
        amod4.insert_transition(q3, 'b', q3)
        amod4.insert_transition(q3, 'a', q0)

        self.assertFalse(evena.is_equal(amod4))

    def test_intersection_disjoint_languages(self):
        q0 = State("q0")
        q1 = State("q1")
        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)

        empty = evena.intersection(evena.complement())

        empty.minimize()

        self.assertTrue(empty.is_empty())

    def test_minimize_empty_complement_automaton(self):
        q0 = State("q0")
        q1 = State("q1")
        evena = FiniteAutomaton({q0, q1}, {'a', 'b'}, q0, {q0})
        evena.insert_transition(q0, 'b', q0)
        evena.insert_transition(q0, 'a', q1)
        evena.insert_transition(q1, 'b', q1)
        evena.insert_transition(q1, 'a', q0)

        complement = evena.complement()

        intersection = evena.intersection(complement)

        intersection = intersection.complement()

        intersection.minimize()

        self.assertFalse(intersection.is_empty())

    def test_minimization_on_the_automaton_language_epsilon_word(self):
        q0 = State("q0")
        q1 = State("q1")
        epsilon_word = FiniteAutomaton({q0, q1}, set(), q0, {q1})
        epsilon_word.insert_transition(q0, '&', q1)

        pdb.set_trace()
        epsilon_word.minimize()

        self.assertTrue(epsilon_word.recognize_sentence(""))
