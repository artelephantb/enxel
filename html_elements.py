def comment_el(el) -> str:
	return f'<!--{el.text}-->'

def text_el(el) -> str:
	return f'<p>{el.text}</p>'
