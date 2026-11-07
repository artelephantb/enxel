from err import ElementDoesNotExistError, AttributeNotFoundError, MismatchedTypesError
from exnel_types import *


def compile_html(
	tag: str,
	content: str,
	attrs: dict,
	attrs_removals=[],
	attrs_overides={},
	single=False,
) -> str:
	html = f'<{tag} '

	final_attrs = attrs
	for remove in attrs_removals:
		del final_attrs[remove]

	for overide_name in attrs_overides:
		final_attrs[overide_name] = attrs_overides[overide_name]

	for attr_name in final_attrs:
		html += f'{attr_name}="{final_attrs[attr_name]}"'

	if single:
		html += f'/>'
	else:
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
		css += prop_name + ':' + str(final_props[prop_name]) + ';'

	return css


class HTMLRenderer:
	def __init__(self, keep_comments=False):
		# TODO: Add user defined elements
		self.defined_elements = {}

		self.keep_comments = False

	def comment_el(self, el) -> str:
		return f'<!--{el.text}-->'

	def text_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		style = compile_css({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px',
			'font-size': str(size) + 'px'
		}, style_removals, style_overides)

		return compile_html('p', el.text, {
			'style': style
		}, html_removals, html_overides)

	def link_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		pos = get_vector2(el, 'pos', '0,0')

		style = compile_css({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px'
		}, style_removals, style_overides)

		to = get_str(el, 'to', '')

		content = el.text
		if not content:
			content = self._render_multiple_elements(el)

		return compile_html('a', content, {
			'href': to,
			'style': style
		}, html_removals, html_overides)

	def image_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		src = get_str(el, 'src')
		draggable = get_bool(el, 'draggable', 'false')

		pos = get_vector2(el, 'pos', '0,0')

		width = 'keep'
		height = 'keep'
		if el.get('scale'):
			scale = get_vector2(el, 'scale')
			width = str(scale.x) + 'px'
			height = str(scale.y) + 'px'

		style = compile_css({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px',
			'width': width,
			'height': height
		}, style_removals, style_overides)

		return compile_html('img', '', {
			'src': src,
			'draggable': draggable,
			'alt': el.text,
			'style': style
		}, html_removals, html_overides, single=True)


	def vcon_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		html = '<div style="display:flex;flex-direction:column">'
		for child in el:
			html_el = self._render_element(child, style_removals=['position', 'left', 'top'])
			html += html_el
		html += '</div>'

		return html

	def hcon_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		html = '<div style="display:flex;flex-direction:row">'
		for child in el:
			html_el = self._render_element(child, style_removals=['position', 'left', 'top'])
			html += html_el
		html += '</div>'

		return html


	def _render_element(self, el, html_overides={}, html_removals=[], style_overides={}, style_removals=[]) -> str:
		# Comment
		if not isinstance(el.tag, str):
			if self.keep_comments:
				return self.comment_el(el)
			return ''

		match el.tag:
			case 'comment':
				return self.comment_el(el)
			case 'text':
				return self.text_el(el, html_overides, html_removals, style_overides, style_removals)
			case 'link':
				return self.link_el(el, html_overides, html_removals, style_overides, style_removals)
			case 'img':
				return self.image_el(el, html_overides, html_removals, style_overides, style_removals)
			case 'vcon':
				return self.vcon_el(el, html_overides, html_removals, style_overides, style_removals)
			case 'hcon':
				return self.hcon_el(el, html_overides, html_removals, style_overides, style_removals)
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
