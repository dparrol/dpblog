"""Rendering lists of blog posts to generate the various pages."""

import os, sys
import util
import jinja2
from post import Post

def getTemplate(name):
    """Get template, given its filename."""
    with open(os.path.join(os.path.dirname(__file__), 'templates', name + '.jinja')) as f:
        return jinja2.Template(f.read())

def renderPost(post):
    """Render a blog post."""
    return getTemplate('post').render(
        title = post.title,
        date = post.date,
        body = jinja2.Markup(post.html),
    )


def renderAll(srcDir, htmlDir):
    """Take all the blog posts in srcDir, render blog to htmlDir."""
    posts = Post.getAll(srcDir)

    # Render pages for each post
    for post in posts:
        filename = os.path.join(htmlDir, post.filename.replace('.md', '.html'))
        with open(filename, 'w') as f:
            print 'Generating', filename
            f.write(util.toutf8(renderPost(post)))

    # Render the various indexes
    # TODO(dparrol): front page
    # TODO(dparrol): index of all posts
    # TODO(dparrol): RSS or atom feed

    # Copy over the whole static resource hierarchy (if any).
    if os.path.exists(os.path.join(srcDir, 'static')):
        print 'Copying static resources'
        shutil.copytree(os.path.join(srcDir, 'static'), os.path.join(htmlDir, 'static'))

if __name__ == '__main__':
    if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
        print 'usage: render.py fromDir toDir'
        print 'Renders blog using source from fromDir. Puts html in toDir.'
        sys.exit(1)
    renderAll(sys.argv[1], sys.argv[2])
