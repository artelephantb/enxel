from lxml import etree

from html_elements import (
	comment_el,
	text_el
)


class ElementDoesNotExistError(Exception):
	def __init__(self, element_tag: str):
		super().__init__(f"Element '{element_tag}' does not exist")

class Enxel:
	def __init__(self, file_bytes: bytes):
		data = b'<root>' + file_bytes + b'</root>'

		parser = etree.XMLParser(remove_blank_text=True)
		self.root = etree.fromstring(data, parser=parser)

		self.element_types = {
			'~comment': comment_el,
			'text': text_el
		}

		# For rendering
		self.keep_comments = False

	@classmethod
	def from_file(cls, path: str):
		with open(path, 'rb') as file:
			return cls(file.read())

	@classmethod
	def from_str(cls, string: str):
		return cls(string.encode('utf-8'))


	def _render_element(self, element) -> str:
		# Comment
		if not isinstance(element.tag, str):
			if self.keep_comments:
				return self.element_types.get('~comment')(element)
			return ''

		element_type = self.element_types.get(element.tag)
		if not element_type:
			raise ElementDoesNotExistError(element.tag)

		return element_type(element)

	def render(self, keep_comments=False) -> str:
		self.keep_comments = keep_comments

		html = '<!DOCTYPE html><html>'
		for child in self.root:
			html_el = self._render_element(child)
			html += html_el
		html += '</html>'

		return html
