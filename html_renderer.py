from err import ElementDoesNotExistError


class HTMLRenderer:
	def __init__(self, keep_comments=False):
		# TODO: Add user defined elements
		self.defined_elements = {}

		self.keep_comments = False

	def comment_el(self, el) -> str:
		return f'<!--{el.text}-->'

	def text_el(self, el, style_overides: dict) -> str:
		pos = el.get('pos', '0,0')
		x, y = pos.split(',')

		size = el.get('size', '16')

		style = ''
		if not style_overides.get('position'):
			style += 'position:absolute;'
		if not style_overides.get('left'):
			style += f'left:{x}px;'
		if not style_overides.get('top'):
			style += f'top:{y}px;'

		return f'<p style="{style}font-size:{size}px">{el.text}</p>'

	def link_el(self, el) -> str:
		pos = el.get('pos', '0,0')
		x, y = pos.split(',')

		to = el.get('to', '')

		return f'<a href="{to}" style="position:absolute;left:{x}px;top:{y}px">{self._render_multiple_elements(el)}</a>'

	def image_el(self, el) -> str:
		src = el.get('src', 'no_image_specified')
		draggable = el.get('draggable', 'false')

		pos = el.get('pos', '0,0')
		x, y = pos.split(',')

		scale = el.get('scale', 'fit-content,fit-content')
		width, height = scale.split(',')

		return f'<img src="{src}" draggable="{draggable}" alt="{el.text}" style="position:absolute;left:{x}px;top:{y}px;width:{width};height:{height}"/>'


	def vbox_el(self, el) -> str:
		html = ''
		for child in el:
			html_el = self._render_element(child, {
				'position': 'cancel',
				'left': 'cancel',
				'top': 'cancel'
			})
			html += html_el

		return html


	def _render_element(self, el, style_overides={}) -> str:
		# Comment
		if not isinstance(el.tag, str):
			if self.keep_comments:
				return self.element_types.get('~comment')(el)
			return ''

		match el.tag:
			case 'comment':
				return self.comment_el(el)
			case 'text':
				return self.text_el(el, style_overides)
			case 'link':
				return self.link_el(el)
			case 'img':
				return self.image_el(el)
			case 'vbox':
				return self.vbox_el(el)
			case _:
				raise ElementDoesNotExistError(el.tag)

	def _render_multiple_elements(self, root) -> str:
		html = ''
		for child in root:
			html_el = self._render_element(child)
			html += html_el

		return html

	def render(self, exnel) -> str:
		html = '<!DOCTYPE html><html>'
		html += self._render_multiple_elements(exnel.root)
		html += '</html>'

		return html
