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
			self.styles[el.tag][child.tag] = (child.attrib, child.text)

	def _parse(self, root):
		for child in root:
			self.styles[child.tag] = {}
			self._parse_element(child)


	def add_from(self, theme):
		'''Adds this theme to another theme, replaces if already there'''
		for key, value in theme.styles.items():
			try:
				self.styles[key].update(value)
			except KeyError:
				self.styles[key] = value


	def get(self, el: str, item: str, default=None) -> object:
		try:
			element_dict = self.styles[el]
			return element_dict.get(item, default)
		except KeyError:
			if not default:
				return self.styles['global'][item]
			return default


class BaseTheme(Theme):
	def __init__(self, base: dict):
		self.styles = base
