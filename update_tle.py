from __future__ import print_function
import requests
import json
import datetime
from calendar import timegm
import time
from redis import StrictRedis
import sys

redis = StrictRedis(host='localhost', port=6379)

# NASA's station FDO updates this page with very precise data. Only using a
# small bit of it for now.
DATA_URL = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"


def update_tle():
    # Open a http request
    req = requests.get(DATA_URL)
    data = req.text

    # parse the HTML
    data = data.split("<PRE>")[1]
    data = data.split("</PRE>")[0]
    data = data.split("Vector Time (GMT): ")[1:]

    for group in data:
        # Time the vector is valid for
        datestr = group[0:17]

        # parse date string
        tm = time.strptime(datestr, "%Y/%j/%H:%M:%S")

        # change into more useful datetime object
        dt = datetime.datetime(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

        # Debug
        # print dt

        # More parsing
        tle = group.split("TWO LINE MEAN ELEMENT SET")[1]
        tle = tle[8:160]
        lines = tle.split('\n')[0:3]

        # Most recent TLE
        now = datetime.datetime.utcnow()

        if (dt - now).days >= 0:
            # Debug Printing
            """
            print dt
            for line in lines:
                print line.strip()
            print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            """

            # Get the TLE as a list: line 0, 1, 2
            tle = [lines[0].strip(), lines[1].strip(), lines[2].strip()]

            # Put in Redis
            redis.set("iss-tle", json.dumps(tle))

            # Set debug info
            info = {
                "message": "success",
                "tle": tle,
                "tle-time": timegm(dt.timetuple()),
                "tle-update": timegm(now.timetuple()),
            }
            redis.set('iss-tle-info', json.dumps(info))
            break


if __name__ == '__main__':
    print("Updating ISS TLE from JSC...")
    try:
        update_tle()
        print("Success!")
    except Exception:
        exctype, value = sys.exc_info()[:2]
        print("Error:", exctype, value)
