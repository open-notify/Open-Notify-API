#!../env/bin/python
"""
Compute ISS position about every once per second.
"""
import ephem
from math import degrees
import json
from redis import StrictRedis
import datetime
from calendar import timegm
import time

# Redis connection
redis = StrictRedis(host='localhost', port=6379)


def get_iss_location():
    """Compute the lat/lon directly under the ISS (RBAR) at a moment in time
    """

    # Load the TLE from redis
    tle = json.loads(redis.get("iss-tle").decode())
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    # Compute "now" with pyephem
    now = datetime.datetime.utcnow()
    iss.compute(now)
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)

    data = {
        "message": "success",
        "iss_position": {
            "latitude":  "%0.4f" % lat,
            "longitude": "%0.4f" % lon,
        },
        "timestamp": timegm(now.timetuple()),
    }
    redis.set('iss-now', json.dumps(data))


# Run forever every 500 ms
if __name__ == '__main__':
    while True:
        get_iss_location()
        time.sleep(0.5)
