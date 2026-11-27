from enum import Enum


class ExpectationError(Exception): pass


class TokenType(Enum):
	HEADING_1 = 0
	HEADING_2 = 1
	HEADING_3 = 2
	HEADING_4 = 3
	HEADING_5 = 4
	HEADING_6 = 5

	BOLD = 6
	ITALIC = 7

	TEXT = 8

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
				case '#': self._heading()
				case '*':
					if self._peak() == '*':
						self._advance()
						self._add_token(TokenType.BOLD)
					else:
						self._add_token(TokenType.ITALIC)
				case _:
					still_on_text = True
			if still_on_text:
				text += self.source[self.current - 1]
			elif text:
				self._add_token(TokenType.TEXT, text)
				text = ''


	def _heading(self):
		level = 1
		while self._peak() == '#':
			self._advance()
			level += 1

		while self._peak() == ' ': self._advance()

		value = ''
		while not self._is_at_end() and self._peak() != '\n':
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
