from enxel import Enxel
from enxel.theme import Theme
from enxel.renderers.htmlcss_renderer import HTMLCSSRenderer


enxel = Enxel.from_file('demo.xml')

theme = Theme.from_file('demo_theme.xml')
enxel.add_theme(theme)

renderer = HTMLCSSRenderer(scripts=['/script.js'])
renderer.render(enxel)

renderer.save_html('output.html')
renderer.save_css('output.css')
