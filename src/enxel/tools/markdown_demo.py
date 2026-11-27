from markdown import Markdown


text = '''
*Italic*
**Bold**
[Alt Text](https://github.com/artelephantb/enxel)
'''

md = Markdown(text)
print(md.tokens)
