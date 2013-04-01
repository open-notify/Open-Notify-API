---
layout: apidoc
name: issnow
title: Open Notify -- API Doc | ISS Current Location
---

# International Space Station Current Location

<http://api.open-notify.org/iss-now/>

The International Space Station is moving at close to 17,500 miles per hour so
it's location changes really fast!


## Overview

This is a simple api to return the current location of the ISS. When fetched it
returns the current latitude and longitude of the space station with a unix
timestamp for the time the location was valid. This API takes no inputs.


## Output

The output is JSON.

{% highlight javascript %}
{
  "message": "success", 
  "data": {
    "timestamp": "%UNIX TIME STAMP%", 
    "iss_position": {
      "latitude": "%CURRENT LATITUDE%", 
      "longitude": "%CURRENT LONGITUDE%"
    }
  }
}
{% endhighlight %}

The `data` payload has a `timestamp` and an `iss_position` object with the latitude
and longitude.


## Poll Rate

Please note that there is an inherent uncertainty in the ISS position models that
is usually larger than one second. In addition the position is only calculated
once per second (the maximum resolution of an integer unix time stamp). So polling
more than 1 Hz would be useless except to add unnessisary strain to the servers.

A single client should try and keep polling to once every 5 seconds or less.


## Examples

Here is an example reading the API in python:

{% highlight python %}
import urllib2
import json

req = urllib2.Request("http://api.open-notify.org/iss-now/")
response = urllib2.urlopen(req)

obj = json.loads(response.read())

print obj['data']['timestamp']
print obj['data']['iss_position']['latitude'], obj['data']['iss_position']['latitude']

# Example prints:
#   1364795862
#   -47.36999493 151.738540034
{% endhighlight %}


