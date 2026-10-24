from lxml import etree


class Enxel:
	def __init__(self, file_bytes: bytes):
		data = b'<root>' + file_bytes + b'</root>'

		parser = etree.XMLParser(remove_blank_text=True)
		self.root = etree.fromstring(data, parser=parser)

	@classmethod
	def from_file(cls, path: str):
		with open(path, 'rb') as file:
			cls(file.read())

	@classmethod
	def from_str(cls, string: str):
		cls(string.encode('utf-8'))
