from enxel import Enxel
from theme import Theme
from godot_renderer import GodotRenderer


enxel = Enxel.from_file('demo.xml')

theme = Theme.from_file('demo_theme.xml')
enxel.add_theme(theme)

renderer = GodotRenderer()
renderer.render(enxel)

renderer.save_tscn('output.tscn')
