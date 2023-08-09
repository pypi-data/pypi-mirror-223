"""
**********************************************************************************************

This module handles generating flask responses.

A flask response is a tuple that consists of:
    - the body
    - return code

**********************************************************************************************
"""

from http import HTTPStatus
import flask
from typing import Tuple, Any

flasktuple = Tuple[Any, HTTPStatus]


def get(output=None) -> flasktuple:
    """Resource successfully GET - the normal return"""
    return _standard_return(output, HTTPStatus.OK)


def updated(output=None) -> flasktuple:
    """Resource was successfully UPDATED"""
    return _standard_return(output, HTTPStatus.OK)


def created(output=None) -> flasktuple:
    """Resource was successfully CREATED"""
    return _standard_return(output, HTTPStatus.CREATED)


def deleted(output=None) -> flasktuple:
    """Resource was successfully DELETED"""
    return _standard_return(output, HTTPStatus.NO_CONTENT)


def bad_request(output=None) -> flasktuple:
    """Client error"""
    return _standard_return(output, HTTPStatus.BAD_REQUEST)

def not_found(output=None) -> flasktuple:
    """Not found error"""
    return _standard_return(output, HTTPStatus.NOT_FOUND)


def forbidden(output=None) -> flasktuple:
    """Forbidden"""
    return _standard_return(output, HTTPStatus.FORBIDDEN)


def internal_error(output=None) -> flasktuple:
    """500 server response"""
    return _standard_return(output, HTTPStatus.INTERNAL_SERVER_ERROR)


def _standard_return(output, response_code: HTTPStatus) -> flasktuple:

    if isinstance(output, type(None)):
        return ('', response_code)
    
    try:
        output_string = flask.jsonify(output)
    except Exception as ex:
        # print(ex)
        output_string = ''

    return (output_string, response_code)




