import redis
import json
import urllib2
import datetime
from calendar import timegm
import time
import os
import sys

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(REDIS_URL)

# NASA's station FDO updates this page with very precise data. Only using a
# small bit of it for now.
url = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"


def update_tle():
    # Open a http request
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()

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
        #print dt

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

            tle = json.dumps([lines[0].strip(), lines[1].strip(), lines[2].strip()])

            r.set("iss_tle", tle)
            r.set("iss_tle_time", timegm(dt.timetuple()))
            r.set("iss_tle_last_update", timegm(now.timetuple()))
            break


if __name__ == '__main__':
    print "Updating ISS TLE from JSC..."
    try:
        update_tle()
    except:
        exctype, value = sys.exc_info()[:2]
        print "Error:", exctype, value
