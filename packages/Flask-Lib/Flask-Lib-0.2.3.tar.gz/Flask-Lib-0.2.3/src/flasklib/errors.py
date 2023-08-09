from __future__ import annotations
import typing
import requests
import flask

FlaskResponseTuple = typing.Tuple[str, int]

class ICustomError(Exception):
    """
    Base custom error interface.
    All child classes must implement get_response.
    """

    def get_response(self) -> FlaskResponseTuple:
        raise NotImplementedError


class RequestError(ICustomError):
    """Return a response for a bad requests.Response """

    def __init__(self, response: requests.Response, *args):
        super().__init__(*args)
        self.response = response
    
    def get_response(self) -> FlaskResponseTuple:
        return (self.response.text, self.response.status_code)
    


def handle_icustom_error(error: ICustomError) -> FlaskResponseTuple:
    """Handle a raised ICustomError exception"""    
    
    return error.get_response()


def add_error_handler(app: flask.Flask):
    """Add the custom error handler to the Flask application."""
    
    app.register_error_handler(ICustomError, handle_icustom_error)
