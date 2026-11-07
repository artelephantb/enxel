from err import ElementDoesNotExistError, AttributeNotFoundError, MismatchedTypesError


def get_attribute(el, attr: str, type, default=None):
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	match type:
		case 'str':
			return value
		case 'int':
			try:
				int(value)
			except ValueError:
				raise MismatchedTypesError(el.tag, 'int', value)
			return value
		case 'bool':
			if value != 'true' and value != 'false':
				raise MismatchedTypesError(el.tag, 'bool', value)
			return value
		case 'array':
			return value.split(',')
		case 'int_array':
			numbers = value.split(',')
			try:
				for number in numbers:
					int(number)
			except ValueError:
				raise MismatchedTypesError(el.tag, 'int_array', value)

			return numbers
		case 'float_array':
			numbers = value.split(',')
			try:
				for number in numbers:
					float(number)
			except ValueError:
				raise MismatchedTypesError(el.tag, 'float_array', value)

			return numbers
		case 'pos':
			numbers = value.split(',')
			if len(numbers) != 2: raise MismatchedTypesError(el.tag, 'pos', value)
			try:
				for number in numbers:
					int(number)
			except ValueError:
				raise MismatchedTypesError(el.tag, 'pos', value)

			return numbers
		case 'scale':
			numbers = value.split(',')
			if len(numbers) != 2: raise MismatchedTypesError(el.tag, 'scale', value)
			try:
				for number in numbers:
					if not number == 'keep':
						int(number)
			except ValueError:
				raise MismatchedTypesError(el.tag, 'pos', value)

			return numbers

def compile_html(
	tag: str,
	content: str,
	attrs: dict,
	attrs_removals=[],
	attrs_overides={}
) -> str:
	html = f'<{tag} '

	final_attrs = attrs
	for remove in attrs_removals:
		del final_attrs[remove]

	for overide_name in attrs_overides:
		final_attrs[overide_name] = attrs_overides[overide_name]

	for attr_name in final_attrs:
		html += attr_name + '=' + final_attrs[attr_name]

	html += f'>{content}</{tag}>'
	return html

def compile_css(
	props: dict,
	props_removals=[],
	props_overides={}
) -> str:
	css = ''

	final_props = props
	for remove in props_removals:
		del final_props[remove]

	for overide_name in props_overides:
		final_props[overide_name] = props_overides[overide_name]

	for prop_name in final_props:
		css += prop_name + ':' + final_props[prop_name] + ';'

	return css


class HTMLRenderer:
	def __init__(self, keep_comments=False):
		# TODO: Add user defined elements
		self.defined_elements = {}

		self.keep_comments = False

	def comment_el(self, el) -> str:
		return f'<!--{el.text}-->'

	def text_el(self, el, style_overides: dict, style_removals: list) -> str:
		x, y = get_attribute(el, 'pos', 'pos', '0,0')
		size = get_attribute(el, 'size', 'int', '16')

		style = ''
		if not style_overides.get('position'):
			style += 'position:absolute;'
		if not style_overides.get('left'):
			style += f'left:{x}px;'
		if not style_overides.get('top'):
			style += f'top:{y}px;'

		style = compile_css({
			'position': 'absolute',
			'left': x + 'px',
			'top': y + 'px',
			'font-size': size + 'px'
		}, style_removals, style_overides)

		return f'<p style="{style}">{el.text}</p>'

	def link_el(self, el) -> str:
		x, y = get_attribute(el, 'pos', 'pos', '0,0')

		to = el.get('to', '')

		return f'<a href="{to}" style="position:absolute;left:{x}px;top:{y}px">{self._render_multiple_elements(el)}</a>'

	def image_el(self, el) -> str:
		src = get_attribute(el, 'src', 'str')
		draggable = get_attribute(el, 'draggable', 'bool', 'false')

		x, y = get_attribute(el, 'pos', 'pos', '0,0')

		width, height = get_attribute(el, 'scale', 'scale', 'keep,keep')

		return f'<img src="{src}" draggable="{draggable}" alt="{el.text}" style="position:absolute;left:{x}px;top:{y}px;width:{width}px;height:{height}px"/>'


	def vcon_el(self, el) -> str:
		html = ''
		for child in el:
			html_el = self._render_element(child, style_removals=['position', 'left', 'top'])
			html += html_el

		return html


	def _render_element(self, el, style_overides={}, style_removals=[]) -> str:
		# Comment
		if not isinstance(el.tag, str):
			if self.keep_comments:
				return self.element_types.get('~comment')(el)
			return ''

		match el.tag:
			case 'comment':
				return self.comment_el(el)
			case 'text':
				return self.text_el(el, style_overides, style_removals)
			case 'link':
				return self.link_el(el)
			case 'img':
				return self.image_el(el)
			case 'vcon':
				return self.vcon_el(el)
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
