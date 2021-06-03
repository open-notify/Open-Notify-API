import ephem
import datetime
from calendar import timegm
from math import degrees
import redis
import json
import os

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)


def get_location():
    """Compute the current location of the ISS"""

    # Get latest TLE from redis
    tle = json.loads(r.get("iss_tle"))
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    # Compute for now
    now = datetime.datetime.utcnow()
    iss.compute(now)
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)
    elev = iss.elevation

    # Return the relevant timestamp and data
    return {"timestamp": timegm(now.timetuple()), "iss_position": {"latitude": lat, "longitude": lon, "elevation": elev}}


def get_tle():
    """Grab the current TLE"""
    return json.loads(r.get("iss_tle"))


def get_tle_time():
    """Grab the current TLE time"""
    return r.get("iss_tle_time")


def get_tle_update():
    """Grab the tle update time"""
    return r.get("iss_tle_last_update")


def get_passes(lon, lat, alt, n):
    """Compute n number of passes of the ISS for a location"""

    # Get latest TLE from redis
    tle = json.loads(r.get("iss_tle"))
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    # Set location
    location = ephem.Observer()
    location.lat = str(lat)
    location.long = str(lon)
    location.elevation = alt

    # Override refration calculation
    location.pressure = 0
    location.horizon = '10:00'

    # Set time now
    now = datetime.datetime.utcnow()
    location.date = now

    # Predict passes
    passes = []
    for p in xrange(n):
        tr, azr, tt, altt, ts, azs = location.next_pass(iss)
        duration = int((ts - tr) * 60 * 60 * 24)
        year, month, day, hour, minute, second = tr.tuple()
        dt = datetime.datetime(year, month, day, hour, minute, int(second))

        if duration > 60:
            passes.append({"risetime": timegm(dt.timetuple()), "duration": duration})

        # Increase the time by more than a pass and less than an orbit
        location.date = tr + 25*ephem.minute

    # Return object
    obj = {"request": {
        "datetime": timegm(now.timetuple()),
        "latitude": lat,
        "longitude": lon,
        "altitude": alt,
        "passes": n,
        },
        "response": passes,
    }

    return obj
