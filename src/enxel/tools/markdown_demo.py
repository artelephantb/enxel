from markdown import Markdown


text = '''
*Italic*
**Bold**
'''

md = Markdown(text)
print(md.tokens)
