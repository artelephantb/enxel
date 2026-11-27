from enum import Enum


class ExpectationError(Exception): pass


class TokenType(Enum):
	HEADING_1 = 0
	HEADING_2 = 1
	HEADING_3 = 2
	HEADING_4 = 3
	HEADING_5 = 4
	HEADING_6 = 5

class Token:
	def __init__(self, token: TokenType, literal):
		self.token = token
		self.literal = literal

	def __repr__(self) -> str:
		return f'<{TokenType(self.token).name}, \'{self.literal}\'>'


class Markdown:
	def __init__(self, markdown: str):
		self.source = markdown
		self.current = 0
		self.tokens = []

		while not self._is_at_end():
			match self._advance():
				case '#': self._heading()

	def _heading(self):
		level = 1
		while self._peak() == '#':
			self._advance()
			level += 1

		while self._peak() == ' ': self._advance()

		value = ''
		while self._peak() != '' and self._peak() != '\n':
			value += self._advance()

		match level:
			case 1:
				self._add_token(TokenType.HEADING_1, value)
			case 2:
				self._add_token(TokenType.HEADING_2, value)
			case 3:
				self._add_token(TokenType.HEADING_3, value)
			case 4:
				self._add_token(TokenType.HEADING_4, value)
			case 5:
				self._add_token(TokenType.HEADING_5, value)
			case 6:
				self._add_token(TokenType.HEADING_6, value)


	def _add_token(self, type: TokenType, literal=None):
		self.tokens.append(Token(type, literal))

	def _is_at_end(self) -> bool:
		return self.current >= len(self.source)

	def _advance(self) -> str:
		value = self.source[self.current]
		self.current += 1
		return value

	def _peak(self) -> str:
		if self._is_at_end(): return ''
		return self.source[self.current]

	def _consume(self, expect: str):
		if self.source[self.current] != expect:
			raise ExpectationError(f'Expected \'{expect}\' got \'{self.source[self.current]}\'')

		self.current += 1
