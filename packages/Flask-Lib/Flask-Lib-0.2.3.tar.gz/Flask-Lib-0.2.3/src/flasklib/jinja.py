import flask
from markupsafe import Markup


class JinjaMacro:

    FOLDER = 'macros'

    def __init__(self, filename: str, macro: str):
        self._file = filename
        self.macro = macro

    @property
    def filename(self) -> str:
        return f'{self.FOLDER}/{self._file}'
    

    def render_html(self, *args) -> Markup:
        # load up the template macro
        jinja_macro = flask.get_template_attribute(self.filename, self.macro)

        # execute the macro
        html = jinja_macro(*args)

        return html


def override_macro_folder(folder: str):
    JinjaMacro.FOLDER = folder

def run_macro(filename: str, macro: str, *args) -> Markup:
    # load up the template macro
    jinja_macro = flask.get_template_attribute(filename, macro)

    # execute the macro
    html = jinja_macro(*args)

    return html