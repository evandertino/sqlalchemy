from __future__ import absolute_import

import os
from scss import Scss

# these docs aren't super accurate
# http://pyscss.readthedocs.org/en/latest/

def add_stylesheet(app):
    to_gen = []
    for static_path in app.env.config.html_static_path:
        path = os.path.join(app.env.srcdir, static_path)
        for fname in os.listdir(path):
            name, ext = os.path.splitext(fname)
            if ext != ".scss":
                continue
            to_gen.append((path, name))

    # sphinx doesn't really have a "temp" area that will persist
    # down into build-finished (env.temp_data gets emptied).
    # So make our own!
    app._builder_scss = to_gen

    for path, name in to_gen:
        app.add_stylesheet('%s.css' % name)

def generate_stylesheet(app, exception):
    to_gen = app._builder_scss

    compiler = Scss(scss_opts={"style": "expanded"})
    for static_path, name in to_gen:

        css = compiler.compile(
            open(os.path.join(static_path, "%s.scss" % name)).read())

        dest = os.path.join(app.builder.outdir, '_static', '%s.css' % name)
        #copyfile(os.path.join(source, "%s.css" % name), dest)

        with open(dest, "w") as out:
            out.write(css)


def setup(app):
    app.connect('builder-inited', add_stylesheet)
    app.connect('build-finished', generate_stylesheet)

