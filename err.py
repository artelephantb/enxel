class ElementDoesNotExistError(Exception):
	def __init__(self, element_tag: str):
		super().__init__(f"Element '{element_tag}' does not exist")
