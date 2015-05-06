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
        self.assertSetEqual('aS', generated)
