#************************************************************************************
# Name:     CustomJSONEncoder
#
# Purpose:  This class is used to encode date's in the correct format: YYYY-MM-DD. 
#
#           Before creating this, Flask was encoding all dates/datetimes/times as 'Mon, 15 Mar 2021 18:30:42 GMT'.
#           This was done to fields that were only dates.
#
#           The solution was found: https://www.javaer101.com/en/article/1732830.html
#************************************************************************************

from flask.json.provider import DefaultJSONProvider
from flask import Flask
from datetime import date, datetime, timedelta
from decimal import Decimal

class CustomJSONEncoder(DefaultJSONProvider):
    """Custon JSON Encoder"""

    compact = False
    sort_keys = False

    @staticmethod
    def default(obj):    
        try:
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, timedelta):
                return timedelta.__str__
        except TypeError:
            pass

        return DefaultJSONProvider.default(obj)
    


def set_json_encoder(app: Flask):
    """Assign the specified Flask application's json encoder"""
    app.json = CustomJSONEncoder(app)
        