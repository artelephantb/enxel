from lxml import etree
from enxel.theme import BaseTheme, Theme


class Enxel:
	def __init__(self, file_bytes: bytes):
		data = b'<root>' + file_bytes + b'</root>'

		parser = etree.XMLParser(remove_blank_text=True)
		self.root = etree.fromstring(data, parser=parser)

		self.theme = BaseTheme({
			'global': {
				'font': 'Serif'
			}
		})

	@classmethod
	def from_file(cls, path: str):
		with open(path, 'rb') as file:
			return cls(file.read())

	@classmethod
	def from_str(cls, string: str):
		return cls(string.encode('utf-8'))


	def add_theme(self, theme: Theme):
		self.theme.add_from(theme)


	def render(self, renderer, keep_comments=False) -> str:
		renderer_instance = renderer(keep_comments=keep_comments)
		return renderer_instance.render(self, self.styles)
