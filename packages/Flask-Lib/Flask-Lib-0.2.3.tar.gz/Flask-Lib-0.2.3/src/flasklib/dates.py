"""
**********************************************************************************************

This module contains all the custom flask url type converters.

See: https://werkzeug.palletsprojects.com/en/2.2.x/routing/#custom-converters

Flask url date converter

**********************************************************************************************
"""

from __future__ import annotations
from enum import Enum
import flask
from werkzeug.routing import BaseConverter, ValidationError
from datetime import date, datetime, time
import typing

DateType = typing.Union[date, datetime, time]

class UrlDateConverter(BaseConverter):
    """
    Flask url date converter.

    See: https://werkzeug.palletsprojects.com/routing#custom-converters
    """
    
    def to_python(self, value) -> date:
        try:
            return date.fromisoformat(value)
        except ValueError as ex:
            raise ValidationError(f'Invalid date value: {value}')

    def to_url(self, date_obj: date) -> str:
        return date_obj.isoformat()



class DateFormatTokens(str, Enum):
    """Custom date formatting values:

        - DATE_LONG       = Tue 07/26/22
        - DAY_OF_THE_WEEK = Tue
        - SLASHES         = 07/26/22
        - TIME            = 10:13 AM
        - ISO_DATE        = 2023-02-07
        - ISO_TIME        = 14:05:26
    """
    
    DATE_LONG       = "%a %x"       # Tue 07/26/22
    DAY_OF_THE_WEEK = "%a"          # Tue
    SLASHES         = "%x"          # 07/26/22
    TIME            = "%I:%M %p"    # 10:13 AM
    ISO_DATE        = "%Y-%m-%d"    # 2023-02-07
    ISO_TIME        = "%H:%M:%S"    # 14:05:26





def register_template_filters(app: flask.Flask):
    """Add format functions, UrlDateConverter, and DateFormatTokens to the jinja engine."""

    # add these functions to jinja engine to use in a template
    app.add_template_filter(format_iso_date_str, format_iso_date_str.__name__)
    app.add_template_filter(format_date, format_date.__name__)

    # add url date converter to application url map
    app.url_map.converters.update(date=UrlDateConverter)

    # add the date format tokens to the jinja engine
    app.jinja_env.globals.update(
        DateFormatTokens = DateFormatTokens,
    )


def format_iso_date_str(day: str, token: DateFormatTokens) -> str:
    """Format the given datetime string to the specified token"""

    d = datetime.fromisoformat(day)
    return format_date(d, token)


def format_date(day: DateType, token: DateFormatTokens) -> str:
    """Format the given datetime object to the specified token"""

    try:
        formatted_date = day.strftime(token.value)
    except ValueError as ex:
        formatted_date = str(ex)
    
    return formatted_date







