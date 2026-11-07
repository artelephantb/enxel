from err import AttributeNotFoundError, MismatchedTypesError


class Vector2:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __str__(self):
		return f'{str(self.x)},{str(self.y)}'

	def __add__(self, other):
		if type(other) != Vector2:
			raise MismatchedTypesError('Vector2', type(other))

		return Vector2(self.x + other.x, self.y + other.y)


def get_str(el, attr: str, default=None) -> str:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	return value

def get_int(el, attr: str, default=None) -> int:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	try:
		return int(value)
	except ValueError:
		raise MismatchedTypesError('int', value)

def get_float(el, attr: str, default=None) -> float:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	try:
		return float(value)
	except ValueError:
		raise MismatchedTypesError('float', value)

def get_bool(el, attr: str, default=None) -> bool:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	if value != 'true' and value != 'false':
		raise MismatchedTypesError('bool', value)
	return value

def get_list(el, attr: str, default=None) -> list:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	return value.split(',')

def get_vector2(el, attr: str, default=None) -> Vector2:
	value = el.get(attr, default)
	if value == None:
		raise AttributeNotFoundError(attr, el.tag)

	value = value.split(',')
	if len(value) > 2:
		raise MismatchedTypesError('Vector2', value)

	try:
		x = int(value[0])
	except ValueError:
		raise MismatchedTypesError('Vector2(int, ...)', value)

	try:
		y = int(value[1])
	except ValueError:
		raise MismatchedTypesError('Vector2(..., int)', value)

	return Vector2(x, y)
