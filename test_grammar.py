import unittest
from grammar import Grammar
from grammar import Production
from grammar import InitialSymbolNotInNonTerminalsSetException

class TestGrammar(unittest.TestCase):

    def setUp(self):
        self.grammar = Grammar()

    def test_create_empty_grammar(self):
        grammar = Grammar()
        self.assertSetEqual(set(), grammar.productions())

    def test_create_production(self):
        production = Production('S', 'aS')
        self.assertEqual('S', production.left())
        self.assertEqual('aS', production.right())

    def test_add_production(self):
        self.grammar.add_production(Production("S", "aS"))
        self.assertEqual(1, self.grammar.productions_quantity())

    def test_create_grammar_with_wrong_initial_symbol(self):
        self.assertRaises(InitialSymbolNotInNonTerminalsSetException, Grammar, {'a'}, {'S'}, 'A')

    def test_generate_in_1_step_1_production(self):
        self.grammar.add_production(Production('S', 'aS'))
        generated = self.grammar.generate()
        self.assertEqual('aS', generated)

    def test_grammar_conversion_ndfa_fa_aaab(self):
        # S -> aS | b
        self.grammar.add_production(Production('S','aS'))
        self.grammar.add_production(Production('S','b'))
        fa = self.grammar.to_finite_automaton()
        # Should accept
        self.assertEqual(True,fa.recognize_sentence('b'));
        self.assertEqual(True,fa.recognize_sentence('ab'));
        self.assertEqual(True,fa.recognize_sentence('aab'));
        self.assertEqual(True,fa.recognize_sentence('aaaaaaaaaaaaab'));
        # Shouldn't accept
        self.assertEqual(False,fa.recognize_sentence(''));
        self.assertEqual(False,fa.recognize_sentence('a'));
        self.assertEqual(False,fa.recognize_sentence('aa'));
        self.assertEqual(False,fa.recognize_sentence('aaaaaaaaaaaaa'));
        self.assertEqual(False,fa.recognize_sentence('ba'));
        self.assertEqual(False,fa.recognize_sentence('abb'));
        self.assertEqual(False,fa.recognize_sentence('abaaaaaaab'));

    def test_grammar_conversion_ndfa_fa_aabbccd(self):
        # S -> aS | bB
        # B -> bB | cC
        # C -> cC | d
        self.grammar.add_production(Production('S','aS'))
        self.grammar.add_production(Production('S','bB'))
        self.grammar.add_production(Production('B','bB'))
        self.grammar.add_production(Production('B','cC'))
        self.grammar.add_production(Production('C','cC'))
        self.grammar.add_production(Production('C','d'))
        fa = self.grammar.to_finite_automaton()
        # Should accept
        self.assertEqual(True,fa.recognize_sentence('abcd'));
        self.assertEqual(True,fa.recognize_sentence('bcd'));
        self.assertEqual(True,fa.recognize_sentence('bbbcccd'));
        self.assertEqual(True,fa.recognize_sentence('aaabbbcccd'));
        self.assertEqual(True,fa.recognize_sentence('aaaabccccd'));
        self.assertEqual(True,fa.recognize_sentence('aaaabcd'));
        # Shouldn't accept
        self.assertEqual(False,fa.recognize_sentence(''));
        self.assertEqual(False,fa.recognize_sentence('abc'));
        self.assertEqual(False,fa.recognize_sentence('acd'));
        self.assertEqual(False,fa.recognize_sentence('abd'));
        self.assertEqual(False,fa.recognize_sentence('aaaaabbbbbcccc'));
        self.assertEqual(False,fa.recognize_sentence('dabc'));
        self.assertEqual(False,fa.recognize_sentence('abdc'));
        self.assertEqual(False,fa.recognize_sentence('adbc'));
        self.assertEqual(False,fa.recognize_sentence('aadbbccd'));
        self.assertEqual(False,fa.recognize_sentence('dabcd'));
        self.assertEqual(False,fa.recognize_sentence('abcdd'));

    def test_grammar_conversion_ndfa_fa_ccababba(self):
        # S -> cS | cA
        # A -> aA | bA | a | b
        self.grammar.add_production(Production('S','cS'))
        self.grammar.add_production(Production('S','cA'))
        self.grammar.add_production(Production('A','aA'))
        self.grammar.add_production(Production('A','bA'))
        self.grammar.add_production(Production('A','a'))
        self.grammar.add_production(Production('A','b'))
        fa = self.grammar.to_finite_automaton()
        # Should accept
        self.assertEqual(True,fa.recognize_sentence('ca'));
        self.assertEqual(True,fa.recognize_sentence('cb'));
        self.assertEqual(True,fa.recognize_sentence('ccccca'));
        self.assertEqual(True,fa.recognize_sentence('cccccb'));
        self.assertEqual(True,fa.recognize_sentence('cab'));
        self.assertEqual(True,fa.recognize_sentence('cba'));
        self.assertEqual(True,fa.recognize_sentence('cbababba'));
        self.assertEqual(True,fa.recognize_sentence('ccccababaaaabbbbbbabaabaabbb'));
        # Shouldn't accept
        self.assertEqual(False,fa.recognize_sentence(''));
        self.assertEqual(False,fa.recognize_sentence('c'));
        self.assertEqual(False,fa.recognize_sentence('cccccc'));
        self.assertEqual(False,fa.recognize_sentence('a'));
        self.assertEqual(False,fa.recognize_sentence('b'));
        self.assertEqual(False,fa.recognize_sentence('babaaab'));
        self.assertEqual(False,fa.recognize_sentence('babababaabc'));
        self.assertEqual(False,fa.recognize_sentence('bababcabaab'));
