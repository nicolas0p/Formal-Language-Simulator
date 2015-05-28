import unittest
from regular_expression import RegularExpression

class TestRegularExpression(unittest.TestCase):

	def test_normalize(self):
		regex = RegularExpression('(ab)*|ab')
		self.assertEqual('(a.b)*|a.b',regex._string)

		regex = RegularExpression('(a)|(b).(c)')
		self.assertEqual('(a)|(b).(c)',regex._string)

		regex = RegularExpression('a|bc')
		self.assertEqual('a|b.c',regex._string)

		regex = RegularExpression('(ab)*(ba)*')
		self.assertEqual('(a.b)*.(b.a)*',regex._string)

		regex = RegularExpression('a(ba)*b')
		self.assertEqual('a.(b.a)*.b',regex._string)

		regex = RegularExpression('(ba|a(ba)*a)*(ab)*')
		self.assertEqual('(b.a|a.(b.a)*.a)*.(a.b)*',regex._string)

		regex = RegularExpression('abab')
		self.assertEqual('a.b.a.b',regex._string)

		regex = RegularExpression('(a*)')
		self.assertEqual('a*',regex._string)

		regex = RegularExpression('(a)*')
		self.assertEqual('(a)*',regex._string)

		regex = RegularExpression('a')
		self.assertEqual('a',regex._string)

		regex = RegularExpression('')
		self.assertEqual('',regex._string)

	def test_get_less_significant(self):
		regex = RegularExpression('(ab)*|ab')
		self.assertEqual(('|',6),regex._get_less_significant())

		regex = RegularExpression('(a)|(b).(c)')
		self.assertEqual(('|',3),regex._get_less_significant())

		regex = RegularExpression('a|bc')
		self.assertEqual(('|',1),regex._get_less_significant())

		regex = RegularExpression('(ab)*(ba)*')
		self.assertEqual(('.',6),regex._get_less_significant())

		regex = RegularExpression('a(ba)*b')
		self.assertEqual(('.',1),regex._get_less_significant())

		regex = RegularExpression('(ba|a(ba)*a)*(ab)*')
		self.assertEqual(('.',17),regex._get_less_significant())

		regex = RegularExpression('abab')
		self.assertEqual(('.',1),regex._get_less_significant())

		regex = RegularExpression('(a*)')
		self.assertEqual(('*',1),regex._get_less_significant())

		regex = RegularExpression('(a)*')
		self.assertEqual(('*',3),regex._get_less_significant())

		regex = RegularExpression('a')
		self.assertEqual(('a',0),regex._get_less_significant())

		regex = RegularExpression('')
		self.assertEqual(('&',-1),regex._get_less_significant())
