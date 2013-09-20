---
layout: apidoc
name: isspass
title: Open Notify -- API Doc | ISS Pass Times
---

# International Space Station Pass Times


The international space station (ISS) is an orbital outpost circling high above
out heads. Sometimes it’s overhead, but when? It depends on your location. Given
a location on Earth (latitude, longitude, and altitude) this API will compute
the next n number of times that the ISS will be overhead.

Overhead is defined as 10&deg; in elevation for the observer. The times are computed
in UTC and the length of time that the ISS is above 10° is in seconds.

This gives you enough information to compute pass times for up to several
weeks, but beware! times are less and less accurate as you go into the future.
This is because the orbit of the ISS decays unpredictably over time and because
station controllers periodically move the station to higher and lower orbits
for docking, re-boost, and debris avoidance.


## Overview

The API returns a list of upcoming ISS passes for a particular location formatted
as JSON.

As input it expects a latitude/longitude pair, altitude and how many results to
return. All fields are required.

As output you get the same inputs back (for checking) and a time stamp when the
API ran in addition to a success or failure message and a list of passes. Each
pass has a duration in seconds and a rise time as a unix time stamp.

## Input

This API has 2 required input values and 2 optional ones.

<table class="table table-hover">
  <thead>
    <tr>
      <th>Inptut</th>
      <th>Description</th>
      <th>Query string</th>
      <th>Valid Range</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Latitude</td>
      <td>The latitude of the place to predict passes</td>
      <td><code>lat</code></td>
      <td><code>-80..80</code></td>
      <td><span class="label label-important">YES</span></td>
    </tr>
    <tr>
      <td>Longitude</td>
      <td>The longitude of the place to predict passes</td>
      <td><code>lon</code></td>
      <td><code>-180..180</code></td>
      <td><span class="label label-important">YES</span></td>
    </tr>
    <tr>
      <td>Altitude</td>
      <td>The altitude of the place to predict passes</td>
      <td><code>alt</code></td>
      <td><code>0..10000</code></td>
      <td><span class="label">No</span></td>
    </tr>

  </tbody>
</table>

## Output

### JSON

<http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON>

{% highlight javascript %}
{
  "message": "success",
  "request": {
    "latitude": LATITUE,
    "longitude": LONGITUDE, 
    "altitude": ALTITUDE,
    "passes": NUMBER_OF_PASSES,
    "datetime": REQUEST_TIMESTAMP
  },
  "response": [
    {"risetime": TIMESTAMP, "duration": DURATION},
    ...
  ]
}
{% endhighlight %}

### JSONP

Appending a callback request to the query string will return JSONP:

<http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON&callback=CALLBACK>

{% highlight javascript %}
CALLBACK({
  "message": "success",
  "request": {
    "latitude": LATITUE,
    "longitude": LONGITUDE, 
    "altitude": ALTITUDE,
    "passes": NUMBER_OF_PASSES,
    "datetime": REQUEST_TIMESTAMP
  },
  "response": [
    {"risetime": TIMESTAMP, "duration": DURATION},
    ...
  ]
})
{% endhighlight %}


The values used to calculate the upcoming passes are returned in
the `request` object. The `response` is a list of the timestamp
or each pass along with the `durateion` in seconds.



