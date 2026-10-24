from lxml import etree


with open('demo.html', 'rb') as file:
	enxel = b'<root>' + file.read() + b'</root>'

parser = etree.XMLParser(remove_blank_text=True)
root = etree.fromstring(enxel, parser=parser)
print(etree.tostring(root))
