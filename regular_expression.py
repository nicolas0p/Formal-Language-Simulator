class RegularExpression:
	def __init__(self, string, terminals = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'}):
		self._string = string
		self._terminals = terminals

	def _normalize(self):
		string = self._string
		pos = 0;
		for i in range(0,len(self._string)-1):
			pair = self._string[i:i+2]

			# "ab" or "a(" or ")a" or "*a" or "*(" or ")("
			if 	( pair[0] in self._terminals and pair[1] in self._terminals ) or \
				( pair[0] in self._terminals and pair[1] == '(' ) or \
				( pair[0] == ')' and pair[1] in self._terminals ) or \
				( pair[0] == '*' and pair[1] in self._terminals ) or \
				( pair[0] == '*' and pair[1] == '(' ) or \
				( pair[0] == ')' and pair[1] == '('):

				string = string[:pos+1] + '.' + string[pos+1:]
				pos = pos + 1

			pos = pos + 1

		self._string = string

	def to_deterministic_finite_automaton(self):
		pass
