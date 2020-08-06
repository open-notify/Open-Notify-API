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

Overhead is defined as 10&deg; in elevation for the observer. The times are
computed in UTC and the length of time that the ISS is above 10&deg; is in
seconds.

This gives you enough information to compute pass times for up to several
weeks, but beware! times are less and less accurate as you go into the future.
This is because the orbit of the ISS decays unpredictably over time and because
station controllers periodically move the station to higher and lower orbits
for docking, re-boost, and debris avoidance.

## Overview

The API returns a list of upcoming ISS passes for a particular location
formatted as JSON.

As input it expects a latitude/longitude pair, altitude and how many results to
return. All fields are required.

As output you get the same inputs back (for checking) and a time stamp when the
API ran in addition to a success or failure message and a list of passes. Each
pass has a duration in seconds and a rise time as a unix time stamp.

## Input

This API has 2 required input values and 2 optional ones.

{: .table .table-hover}
Inptut | Description | Query string | Valid Range | Units | Required?
---------- | -------------------------------------------- | ------------ | ----------- | ------- | ---------
_Latitude_ | The latitude of the place to predict passes | `lat` | `-80..80` | degrees | <span class="label label-important">YES</span>
_Longitude_ | The longitude of the place to predict passes | `lon` | `-180..180` | degrees | <span class="label label-important">YES</span>
_Altitude_ | The altitude of the place to predict passes | `alt` | `0..10,000` | meters | <span class="label">No</span>
_Number_ | The number of passes to return | `n` | `1..100` | &ndash; | <span class="label">No</span>

## Output

### JSON

<http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON>

```json
{
  "message": "success",
  "request": {
    "latitude": LATITUDE,
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
```

### JSONP

Appending a callback request to the query string will return JSONP:

<http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON&callback=CALLBACK>

```javascript
CALLBACK({
  "message": "success",
  "request": {
    "latitude": LATITUDE,
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
```

The values used to calculate the upcoming passes are returned in
the `request` object. The `response` is a list of the timestamp
or each pass along with the `duration` in seconds.
