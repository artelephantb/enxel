from err import ElementDoesNotExistError, AttributeNotFoundError, MismatchedTypesError
from exnel_types import *

from uid_generator import generate_uid


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

def compile_css_class(
	props: dict,
	name: str,
	props_removals=[],
	props_overides={},
	cases=[]
) -> str:
	final = name
	for case in cases:
		final += '::' + case

	final += '{'
	final += compile_css(
		props,
		props_removals=props_removals,
		props_overides=props_overides
	)
	final += '}'

	return final


class HTMLCSSRenderer:
	def __init__(self, keep_comments=False, embed_css=False, css_link_path='/output.css'):
		# TODO: Add user defined elements
		self.defined_elements = {}

		self.keep_comments = False
		self.embed_css = embed_css
		self.css_link_path = css_link_path

		self.exnel = None

		self.html = ''
		self.css = ''


	def comment_el(self, el) -> str:
		return f'<!--{el.text}-->'

	def text_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		uid = generate_uid()

		self.css += compile_css_class({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px',
			'font-size': str(size) + 'px',
			'font-family': self.exnel.theme.get('text', 'font')[1].removeprefix('[SYS] ')
		}, '.' + uid, style_removals, style_overides)

		return compile_html('p', el.text, {
			'class': uid
		}, html_removals, html_overides)

	def link_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		pos = get_vector2(el, 'pos', '0,0')

		uid = generate_uid()

		self.css += compile_css_class({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px',
			'font-family': self.exnel.theme.get('link', 'font')[1].removeprefix('[SYS] ')
		}, '.' + uid, style_removals, style_overides)

		to = get_str(el, 'to', '')

		content = el.text
		if not content:
			content = self._render_multiple_elements(el)

		return compile_html('a', content, {
			'href': to,
			'class': uid
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

		uid = generate_uid()

		self.css += compile_css_class({
			'position': 'absolute',
			'left': str(pos.x) + 'px',
			'top': str(pos.y) + 'px',
			'width': width,
			'height': height
		}, '.' + uid, style_removals, style_overides)

		return compile_html('img', '', {
			'src': src,
			'draggable': draggable,
			'alt': el.text,
			'class': uid
		}, html_removals, html_overides, single=True)


	def vcon_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		html = '<div style="display:flex;flex-direction:column">'
		for child in el:
			html_el = self._render_element(child, style_removals=['position', 'left', 'top'])
			html += html_el
		html += '</div>'

		return html

	def hcon_el(self, el, html_overides: dict, html_removals: list, style_overides: dict, style_removals: list) -> str:
		align_items = get_str(el, 'align-items', 'left')

		html = f'<div style="display:flex;flex-direction:row;justify-content:{align_items}">'
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

	def render(self, exnel):
		self.exnel = exnel

		body = self._render_multiple_elements(exnel.root)

		# TODO Make colors better
		background_color = exnel.theme.get('background', 'color', default=({'type':'hex'}, '#fffff'))
		self.css += compile_css_class(
			{
				'background-color': background_color[1]
			},
			'body'
		)

		html = '<!DOCTYPE html><html>'

		if self.embed_css:
			html += f'<style>{self.css}</style>'
		else:
			html += f'<link rel="stylesheet" href="{self.css_link_path}"/>'

		html += body
		html += '</html>'

		self.html = html

	def save_html(self, path: str):
		with open(path, 'w') as file:
			file.write(self.html)

	def save_css(self, path: str):
		'''Note: Only works when embed_css flag is set'''
		with open(path, 'w') as file:
			file.write(self.css)
