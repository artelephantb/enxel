from enxel import Enxel
from theme import Theme
from html_renderer import HTMLRenderer


enxel = Enxel.from_file('demo.xml')

theme = Theme.from_file('demo_theme.xml')
enxel.set_theme(theme)

output = enxel.render(HTMLRenderer)

with open('output.html', 'w') as file:
	file.write(output)
