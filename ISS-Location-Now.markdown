---
layout: apidoc
name: issnow
title: Open Notify -- API Doc | ISS Current Location
---

# International Space Station Current Location

<http://api.open-notify.org/iss-now.json>

The [International Space Station](http://en.wikipedia.org/wiki/International_Space_Station)
is moving at close to 28,000 km/h so its location changes really fast! Where
is it right now?


## Overview

This is a simple api to return the current location of the ISS. It
returns the current latitude and longitude of the space station with a unix
timestamp for the time the location was valid. This API takes no inputs.


## Output

### JSON

<http://api.open-notify.org/iss-now.json>

{% highlight javascript %}
{
  "message": "success", 
  "timestamp": UNIX_TIME_STAMP, 
  "iss_position": {
    "latitude": CURRENT_LATITUDE, 
    "longitude": CURRENT_LONGITUDE
  }
}
{% endhighlight %}

The `data` payload has a `timestamp` and an `iss_position` object with the latitude
and longitude.

### JSONP

Appending a callback request to the query string will return JSONP:

<http://api.open-notify.org/iss-now.json?callback=CALLBACK>

{% highlight javascript %}
CALLBACK({
  "message": "success", 
  "timestamp": UNIX_TIME_STAMP,
  "iss_position": {
    "latitude": CURRENT_LATITUDE, 
    "longitude": CURRENT_LONGITUDE
  }
})
{% endhighlight %}


## Poll Rate

Please note that there is an inherent uncertainty in the ISS position models that
is usually larger than one second. In addition the position is only calculated
once per second (the maximum resolution of an integer unix time stamp). So polling
more than 1 Hz would be useless except to add unnessisary strain to the servers.

A single client should try and keep polling to about once every 5 seconds.


## Examples

Here is an example reading the API in python:

{% highlight python %}
import urllib2
import json

req = urllib2.Request("http://api.open-notify.org/iss-now.json")
response = urllib2.urlopen(req)

obj = json.loads(response.read())

print obj['timestamp']
print obj['iss_position']['latitude'], obj['data']['iss_position']['latitude']

# Example prints:
#   1364795862
#   -47.36999493 151.738540034
{% endhighlight %}


## Data Source

The ISS is tracked by several agencys. Both [NORAD](http://www.norad.mil/)
and NASA periodically publish data about the station. I scrape this page
for this API:

 - <http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html>

Another popular site for tacking data is celstrak which published NORAD
TLE's:

 - <http://www.celestrak.com/NORAD/elements/stations.txt>

In both cases a "[Two Line Element](http://en.wikipedia.org/wiki/Two-line_element_set)"
is used, which contains enough
infomation about an orbit to calculate an objects postition at any
time within a useful window of accuracy centered around the TLE's
publish date. I try to update the TLE at least once a day.
