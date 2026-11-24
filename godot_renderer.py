from err import ElementDoesNotExistError, AttributeNotFoundError, MismatchedTypesError
from enxel_types import *

from uid_generator import generate_uid, generate_uid_numbers


def get_counter(self, item, name):
	self.counters[item] += 1
	if self.counters[item] == 0:
		return name
	else:
		return name + str(self.counters[item])


class GodotRenderer:
	def __init__(self):
		# TODO: Add user defined elements
		self.defined_elements = {}
		self.counters = {
			'text': -1
		}

		self.enxel = None

		self.scene = f'[gd_scene format=3 uid="uid://{generate_uid()}"]'


	def text_el(self, el, tree=None) -> str:
		tree_str = ''
		if tree:
			tree_str = f' parent="{tree}"'

		pos = get_vector2(el, 'pos', '0,0')
		size = get_int(el, 'size', '16')

		uid = generate_uid()

		self.scene += f'\n\n[sub_resource type="LabelSettings" id="LabelSettings_{uid}"]\n'
		self.scene += f'font_size = {size}'

		body = f'\n\n[node name="{get_counter(self, 'text', 'Label')}" type="Label"{tree_str} unique_id={generate_uid_numbers()}]\n'
		body += f'text = "{el.text}"\n'
		body += f'label_settings = SubResource("{'LabelSettings_' + uid}")'

		return body


	def _render_element(self, el, tree=None) -> str:
		# Comment
		if not isinstance(el.tag, str):
			return ''

		match el.tag:
			case 'text':
				return self.text_el(el, tree)
			case _:
				raise ElementDoesNotExistError(el.tag)

	def _render_multiple_elements(self, root) -> str:
		html = ''
		for child in root:
			html_el = self._render_element(child)
			html += html_el

		return html

	def render(self, enxel):
		self.enxel = enxel

		body = self._render_multiple_elements(enxel.root)
		self.scene += body

	def save_tscn(self, path: str):
		with open(path, 'w') as file:
			file.write(self.scene)
