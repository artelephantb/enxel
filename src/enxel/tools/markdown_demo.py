from markdown import Markdown


text = '''
# Hello!
*Italic*
**Bold**
'''

md = Markdown(text)
print(md.tokens)
