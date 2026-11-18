from lxml import etree


class Theme:
	def __init__(self, file_bytes: bytes):
		data = b'<root>' + file_bytes + b'</root>'

		parser = etree.XMLParser(remove_blank_text=True)
		root = etree.fromstring(data, parser=parser)

		self.styles = {}
		self._parse(root)


	@classmethod
	def from_file(cls, path: str):
		with open(path, 'rb') as file:
			return cls(file.read())

	@classmethod
	def from_str(cls, string: str):
		return cls(string.encode('utf-8'))


	def _parse_element(self, el):
		for child in el:
			self.styles[el.tag][child.tag] = child.text

	def _parse(self, root):
		for child in root:
			self.styles[child.tag] = {}
			self._parse_element(child)


	def add_to(self, to: dict):
		'''Adds this theme to another theme, replaces is already there'''
		for key, value in self.styles.items():
			try:
				to[key].update(value)
			except KeyError:
				to[key] = value
