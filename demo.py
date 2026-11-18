from enxel import Enxel
from html_renderer import HTMLRenderer


en = Enxel.from_file('demo.xml')
output = en.render(HTMLRenderer)

with open('output.html', 'w') as file:
	file.write(output)
