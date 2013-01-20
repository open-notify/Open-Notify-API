import ephem
import datetime
from calendar import timegm
from math import degrees
import redis
import json

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

def get_location():

    tle = json.loads(r.get("iss_tle"))

    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

    now = datetime.datetime.utcnow()
    iss.compute(now)
    lon = degrees(iss.sublong)
    lat = degrees(iss.sublat)

    return {"timestamp": timegm(now.timetuple()), "iss_position": {"latitude": lat, "longitude": lon} }
