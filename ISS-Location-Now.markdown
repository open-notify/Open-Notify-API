---
layout: apidoc
title: Open Notify -- API Doc | ISS Current Location
---

# International Space Station Current Location

<http://api.open-notify.org/iss-now/>

The International Space Station is moving at close to 17,500 miles per hour so
it's location changes really fast!


## Overview

This is a simple api to return the current location of the ISS. When fetched it
returns the current latitude and longitude of the space station with a unix
timestamp that it was valid for. There are no parameters to the API

## Output

The output is JSON. It has a message object that should say success unless something
went wrong on my end. There is a timestamp which is in unix time and iss_position
which has a latitude longitude pair.


{% highlight javascript %}
{
    "timestamp": %a unix time stamp%,
    "message": "success",
    "iss_position":
      {
          "latitude": %The latitude in decimal degress%,
          "longitude": %The longitude in decimal degress%
      }
}
{% endhighlight %}


