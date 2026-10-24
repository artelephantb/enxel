from err import ElementDoesNotExistError


class HTMLRenderer:
	def __init__(self, keep_comments=False):
		# TODO: Add user defined elements
		self.defined_elements = {}

		self.keep_comments = False

	def comment_el(self, el) -> str:
		return f'<!--{el.text}-->'

	def text_el(self, el) -> str:
		pos = el.get('pos', '0,0')
		x, y = pos.split(',')

		size = el.get('size', '16')

		return f'<p style="position:absolute;left:{x}px;top:{y}px;font-size:{size}px">{el.text}</p>'

	def image_el(self, el) -> str:
		src = el.get('src', 'no_image_specified')
		draggable = el.get('draggable', 'false')

		pos = el.get('pos', '0,0')
		x, y = pos.split(',')

		scale = el.get('scale', 'fit-content,fit-content')
		width, height = scale.split(',')

		return f'<img src="{src}" draggable="{draggable}" alt="{el.text}" style="position:absolute;left:{x}px;top:{y}px;width:{width};height:{height}"/>'


	def _render_element(self, el) -> str:
		# Comment
		if not isinstance(el.tag, str):
			if self.keep_comments:
				return self.element_types.get('~comment')(el)
			return ''

		match el.tag:
			case 'comment':
				return self.comment_el(el)
			case 'text':
				return self.text_el(el)
			case 'img':
				return self.image_el(el)
			case _:
				raise ElementDoesNotExistError(el.tag)

	def render(self, exnel) -> str:
		html = '<!DOCTYPE html><html>'
		for child in exnel.root:
			html_el = self._render_element(child)
			html += html_el
		html += '</html>'

		return html
