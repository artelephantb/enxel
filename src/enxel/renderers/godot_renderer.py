from enxel.err import ElementDoesNotExistError, AttributeNotFoundError, MismatchedTypesError
from enxel.enxel_types import *

from enxel.uid_generator import generate_uid, generate_uid_numbers


def get_counter(self, item, name) -> str:
	self.counters[item] += 1
	if self.counters[item] == 0:
		return name
	else:
		return name + str(self.counters[item])

def get_parent(tree: str) -> str:
	if tree:
		return f'parent="{tree}"'
	return 'parent="."'


class GodotRenderer:
	def __init__(self):
		# TODO: Add user defined elements
		self.defined_elements = {}
		self.counters = {
			'text': -1,
			'link': -1,
			'vcon': -1,
			'hcon': -1
		}

		self.enxel = None

		self.scene = f'[gd_scene format=3 uid="uid://{generate_uid()}"]'


	def text_el(self, el, tree: str) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		uid = generate_uid()

		self.scene += f'\n\n[sub_resource type="LabelSettings" id="LabelSettings_{uid}"]\n'
		self.scene += f'font_size = {size}'

		body = f'\n\n[node name="{get_counter(self, 'text', 'Label')}" type="Label" {get_parent(tree)} unique_id={generate_uid_numbers()}]\n'
		body += f'text = "{el.text}"\n'
		body += f'label_settings = SubResource("{'LabelSettings_' + uid}")'

		return body

	def link_el(self, el, tree: str) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		uid = generate_uid()

		self.scene += f'\n\n[sub_resource type="LabelSettings" id="LabelSettings_{uid}"]\n'
		self.scene += f'font_size = {size}'
		self.scene += f'font_color = Color(0, 255, 255, 1)'

		body = f'\n\n[node name="{get_counter(self, 'link', 'Link')}" type="Label" {get_parent(tree)} unique_id={generate_uid_numbers()}]\n'
		body += f'text = "{el.text}"\n'
		body += f'label_settings = SubResource("{'LabelSettings_' + uid}")'

		return body

	def vcon_el(self, el, tree: str) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		align_items = get_str(el, 'align-items', 'start')
		match align_items:
			case 'start': align_items = '0'
			case 'middle': align_items = '1'
			case 'end': align_items = '2'

		uid = generate_uid()

		name = get_counter(self, 'vcon', 'VBoxContainer')

		body = f'\n\n[node name="{name}" type="VBoxContainer" {get_parent(tree)} unique_id={generate_uid_numbers()}]\n'
		body += 'layout_mode = 1\n'
		body += 'anchors_preset = 15\n'
		body += f'alignment = {align_items}'

		for child in el:
			body += self._render_element(child, tree + f'/{name}')

		return body

	def hcon_el(self, el, tree: str) -> str:
		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		align_items = get_str(el, 'align-items', 'start')
		match align_items:
			case 'start': align_items = '0'
			case 'middle': align_items = '1'
			case 'end': align_items = '2'

		uid = generate_uid()

		name = get_counter(self, 'hcon', 'HBoxContainer')

		body = f'\n\n[node name="{name}" type="HBoxContainer" {get_parent(tree)} unique_id={generate_uid_numbers()}]\n'
		body += 'layout_mode = 1\n'
		body += 'anchors_preset = 15\n'
		body += f'alignment = {align_items}'

		tree_name = name
		if tree:
			tree_name = '/' + name

		for child in el:
			body += self._render_element(child, tree + tree_name)

		return body


	def _render_element(self, el, tree: str) -> str:
		# Comment
		if not isinstance(el.tag, str):
			return ''

		match el.tag:
			case 'connect':
				# TODO Add connection support
				return ''
			case 'text':
				return self.text_el(el, tree)
			case 'link':
				# TODO Fix links
				return self.link_el(el, tree)
			case 'img':
				# TODO Add image support
				return ''
			case 'vcon':
				return self.vcon_el(el, tree)
			case 'hcon':
				return self.hcon_el(el, tree)
			case _:
				raise ElementDoesNotExistError(el.tag)

	def _render_multiple_elements(self, root) -> str:
		html = ''
		for child in root:
			html_el = self._render_element(child, '')
			html += html_el

		return html

	def render(self, enxel):
		self.enxel = enxel

		body = f'\n\n[node name="Control" type="Control" unique_id={generate_uid_numbers()}]\n'
		body += 'layout_mode = 3\n'
		body += 'anchors_preset = 15'

		body += self._render_multiple_elements(enxel.root)
		self.scene += body

	def save_tscn(self, path: str):
		with open(path, 'w') as file:
			file.write(self.scene)
