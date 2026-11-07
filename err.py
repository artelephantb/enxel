class ElementDoesNotExistError(Exception):
	def __init__(self, element_tag: str):
		super().__init__(f"Element '{element_tag}' does not exist")

class AttributeNotFoundError(Exception):
	def __init__(self, element_tag: str, attribute: str):
		super().__init__(f"Attribute '{attribute}' not found on '{element_tag}'")

class MismatchedTypesError(Exception):
	def __init__(self, element_tag: str, expected: str, found: str):
		super().__init__(f"Mismatched types (expected {expected}, found '{found}') on '{element_tag}'")
