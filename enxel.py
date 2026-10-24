from lxml import etree


class Enxel:
	def __init__(self, file_bytes: bytes):
		data = b'<root>' + file_bytes + b'</root>'

		parser = etree.XMLParser(remove_blank_text=True)
		self.root = etree.fromstring(data, parser=parser)

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
				return f'<!--{element.text}-->'
			return ''

		# TODO
		el = etree.Element(element.tag)
		el.text = element.tag
		return f'<{element.tag}>{element.text}</{element.tag}>'

	def render(self, keep_comments=False) -> str:
		self.keep_comments = keep_comments

		html = ''
		for child in self.root:
			html_el = self._render_element(child)
			html += html_el

		return html
