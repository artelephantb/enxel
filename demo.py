from enxel import Enxel


en = Enxel.from_file('demo.html')
output = en.render()

print(output)
