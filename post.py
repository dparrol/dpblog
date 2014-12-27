"""Blog posts!"""

import os
import util
from markdown import Markdown
from dateutil.parser import parse as dateparse

# What extensions to use for Markdown formatting
EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.meta',
]

class Post(object):
    """A blog post."""

    def __init__(self, markdown, filename=None):
        self.markdown = util.tounicode(markdown)
        self.filename = filename
        self.href = filename.replace('.md', '.html') if filename else None
        md = Markdown(extensions=EXTENSIONS, output_format='html5', safe_mode=False, lazy_ol=False)
        self.html = util.tounicode(md.convert(self.markdown))
        self.meta = md.Meta
        # A few fields are derived from the metadata.
        self.title = self._meta('title')
        self.date = dateparse(self._meta('date'))

    @classmethod
    def getAll(cls, path):
        posts = []
        for filename in os.listdir(path):
            if filename.endswith('.md') and not filename.endswith('README.md'):
                with open(os.path.join(path, filename)) as f:
                    data = f.read()
                posts.append(cls(data, filename=filename))
        posts.sort(key=lambda p: (p.date, p.title), reverse=True)
        return posts
        
    def _meta(self, field, **kwargs):
        """Get field from metadata, or report error if 'default' kwarg not given."""
        try:
            return self.meta[field][0]
        except (KeyError, IndexError):
            if 'default' in kwargs:
                return kwargs['default']
            else:
                raise KeyError('Required metadata not found: %s' % field)

    def __repr__(self):
        return '<Post: %r on %r>' % (self.title, self.date)
