from lxml import etree


with open('demo.html', 'rb') as file:
	enxel = b'<root>' + file.read() + b'</root>'

root = etree.fromstring(enxel)
print(etree.tostring(root))
