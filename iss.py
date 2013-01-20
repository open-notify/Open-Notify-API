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

    tle = json.loads(r.get("iss_tle"))

    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    now = datetime.datetime.utcnow()
    iss.compute(now)
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)

    return {"timestamp": timegm(now.timetuple()), "iss_position": {"latitude": lat, "longitude": lon} }
