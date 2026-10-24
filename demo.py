from enxel import Enxel
from html_renderer import HTMLRenderer


en = Enxel.from_file('demo.html')
output = en.render(HTMLRenderer)

print(output)
