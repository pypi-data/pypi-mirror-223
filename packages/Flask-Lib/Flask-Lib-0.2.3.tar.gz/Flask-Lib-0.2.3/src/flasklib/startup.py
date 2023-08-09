
import flask
from .dates import register_template_filters
from .errors import add_error_handler
from .json import set_json_encoder


class FlaskLibStartup:
    """Class that does all the setup work."""

    def __init__(self, app: flask.Flask):
        self.app = app

    def setup_app(self):
        register_template_filters(self.app)
        add_error_handler(self.app)
        set_json_encoder(self.app)
