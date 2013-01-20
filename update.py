import redis
import json 
import urllib2
import datetime
import time

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)


# NASA's station FDO updates this page with very precise data. Only using a 
# small bit of it for now.
url = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"

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

        tle = json.dumps( [lines[0].strip()
                         , lines[1].strip()
                         , lines[2].strip()])

        r.set("iss_tle", tle)
