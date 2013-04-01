---
layout: apidoc
name: isspass
title: Open Notify -- API Doc | ISS Pass Times
---

# International Space Station Pass Times

<http://api.open-notify.org/iss/>

The international space station (ISS) is an orbital outpost circling high above
out heads. Sometimes it’s overhead, but when? It depends on your location. Given
a location on Earth (latitude, longitude, and altitude) this API will compute
the next n number of times that the ISS will be overhead.

Overhead is defined as 10° in elevation for the observer. The times are computed
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


