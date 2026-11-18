from enxel import Enxel
from theme import Theme
from htmlcss_renderer import HTMLCSSRenderer


enxel = Enxel.from_file('demo.xml')

theme = Theme.from_file('demo_theme.xml')
enxel.add_theme(theme)

renderer = HTMLCSSRenderer(embed_css=False)
renderer.render(enxel)

renderer.save_html('output.html')
renderer.save_css('output.css')
