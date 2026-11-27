from enum import Enum


class ExpectationError(Exception): pass


class TokenType(Enum):
	BOLD = 0
	ITALIC = 1

	TEXT = 2
	LINK = 3

class Token:
	def __init__(self, token: TokenType, literal):
		self.token = token
		self.literal = literal

	def __repr__(self) -> str:
		if self.literal:
			return f'<{TokenType(self.token).name}, \'{self.literal}\'>'
		else:
			return f'<{TokenType(self.token).name}>'


class Markdown:
	def __init__(self, markdown: str):
		self.source = markdown
		self.current = 0
		self.tokens = []

		text = ''
		while not self._is_at_end():
			still_on_text = False
			match self._advance():
				case '\n': pass
				case '\\': self._advance()
				case '*':
					if self._peak() == '*':
						self._advance()
						self._add_token(TokenType.BOLD)
					else:
						self._add_token(TokenType.ITALIC)
				case '[': self._link()
				case _:
					still_on_text = True
			if still_on_text:
				text += self.source[self.current - 1]
			elif text:
				self._add_token(TokenType.TEXT, text)
				text = ''

	def _link(self):
		alt = ''
		while self._peak() != ']' and not self._is_at_end():
			alt += self._advance()
		self._consume(']')

		self._consume('(')
		link = ''
		while self._peak() != ')' and not self._is_at_end():
			link += self._advance()
		self._consume(')')

		self._add_token(TokenType.LINK, link)


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
