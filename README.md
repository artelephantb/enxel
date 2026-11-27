![Screenshot of the demo page](screenshot.png)
```xml
<hcon align-items='center'>
	<vcon>
		<text size='50'>Enxel</text>
		<link to='https://github.com/artelephantb/enxel'>> GitHub Page</link>
		<text>Enxel is a free and open source way to write better UI faster. This example document shows the current capabilities of Enxel!</text>
		<hcon align-items='center'>
			<img src='enxel.jpg'></img>
		</hcon>
	</vcon>
</hcon>
```

# Renderers
- **HTML/CSS Renderer**: Renders both HTML and CSS
- **Godot Renderer**: Renders Godot (UI) scenes

# Elements
## Script Connection (connect)
On events (like a button pressed), it will call some code (separate to each renderer).

## Text (text)
A readable string.

## Link (link)
A button, usually to go to another page or website.

## Image (img)
Displays an image.

## Vertical Container (vcon)
Puts child elements side-by-side vertically.

## Horizontal Container (hcon)
Puts child elements side-by-side horizontally.

# Elements Todo
- [ ] Audio
- [ ] Bold
- [ ] Button
- [ ] Canvas
- [ ] Strike-through
- [ ] Collapsible Container
- [ ] Something like HTML div
- [ ] Separator
- [ ] Embed
- [ ] Italic
- [ ] List
- [ ] Dropdown
- [x] Text
- [x] Image
- [ ] Subscript
- [ ] Superscript
- [ ] Underline
- [ ] Progress Bar
- [ ] Math
- [ ] SVG
- [ ] Video
