# Convert markdown post to HTML.

import jinja2
from markdown import Markdown
import os, sys

def getTemplate(name):
    """Get template, given its filename."""
    with open(os.path.join(os.path.dirname(__file__), 'templates', name + '.jinja')) as f:
        return jinja2.Template(f.read())

def markdown(src):
    """Convert Markdown to HTML that we can stick in jinja. Return html and metadata."""
    md = Markdown(
        extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.meta'],
        output_format='html5', safe_mode=False, lazy_ol=False)
    html = md.convert(src)
    return jinja2.Markup(html), md.Meta
    
def render(src):
    """Render a blog post to HTML."""
    if not isinstance(src, unicode):
        src = src.decode('utf8')
    body, metadata = markdown(src)
    return getTemplate('post').render(title=metadata['title'][0], body=body)

def main():
    inname, outname = sys.argv[1:3]
    with open(inname) as i:
        with open(outname, 'w') as o:
            o.write(render(i.read()).encode('utf8'))

if __name__ == '__main__':
    main()
