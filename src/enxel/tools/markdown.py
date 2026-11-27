from enum import Enum


class TokenType(Enum):
	HEADING = 0

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
				case '#':
					literal = ''
					while self._peak() == '#':
						literal += self._advance()
					self._add_token(TokenType.HEADING, literal)


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

	def _consume(self):
		self.current += 1
