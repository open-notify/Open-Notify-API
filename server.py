"""
Open-Notify API Entry Point.
============================

This is not a web server itself, it sets up a object (falcon.API) that speaks
the wsgi protocol. This is natively supported by first-class web servers like
nginx.

Typical usage:

    outside world --> nginx --(proxy_pass)--> uwsgi -----> this code


This file should do very little. We just want to initialize redis then build
the HTTP routing table.
"""
from falcon import API
from falcon import HTTP_200, HTTP_503
from redis import StrictRedis

# Global redis connection
redis = StrictRedis(host='localhost', port=6379)

# Missing key error response
ERROR_MISSING = '{"message": "error", "reason": "Service temporarily unavailable"}'


class OpenNotify():
    """Base Class to handle API GET requests.

    Basic GET from redis. Take response, sets headers, looks for a callback
    param to make a JSONP request.

    :param str redis_key: Key in redis that holds the response for this endpoint
    """

    def __init__(self, redis_key):
        self.redis_key = redis_key

    def on_get(self, request, response):
        # COREs header
        response.set_header("Access-Control-Allow-Origin", "*")

        # Lookup Info, set up error if it's missing
        json_string = redis.get(self.redis_key)
        if not json_string:
            response.status = HTTP_503
            data = ERROR_MISSING
        else:
            data = json_string
            response.status = HTTP_200

        # Look for JSONP request, and wrap reply
        callback = request.get_param('callback', None)
        if callback:
            response.body = "%s(%s)" % (callback, data)
            response.content_type = "application/javascript"
        else:
            response.body = data
            response.content_type = "application/json"


# Falcon API instance
api = API()

# Route Table:
# Current ISS Location:
ISSNOW = OpenNotify('iss-now')
api.add_route("/iss-now.json", ISSNOW)
api.add_route("/iss-now/", ISSNOW)
api.add_route("/iss-now/v1/", ISSNOW)

# TLE Debug info:
ISSTLE = OpenNotify('iss-tle-info')
api.add_route("/iss-tle-info.json", ISSTLE)

# How Many People In Space
ASTROS = OpenNotify('people-in-space')
api.add_route("/astros.json", ASTROS)
api.add_route("/astros/", ASTROS)
api.add_route("/astros/v1/", ASTROS)
