---
layout: page
name: apidoc
title: Open Notify -- API Documentation
---

# API Documentation

## Current ISS Location

The [International Space Station](http://en.wikipedia.org/wiki/International_Space_Station)
is moving at close to 28,000 km/h so its location changes really fast! Where
is it right now?

**Documentation: [ISS Location Now](ISS-Location-Now)**

### Example:

{% include iss-now_map.html %}

Using leaflet and jquery one can write a script to show the current location of
the ISS and update it every 5 seconds:

{% highlight javascript %}
function moveISS () {
    $.getJSON('http://api.open-notify.org/iss-now.json?callback=?', function(data) {
        var lat = data['iss_position']['latitude'];
        var lon = data['iss_position']['longitude'];

        iss.setLatLng([lat, lon]);
        isscirc.setLatLng([lat, lon]);
        map.panTo([lat, lon], animate=true);
    });
    setTimeout(moveISS, 5000); 
}
{% endhighlight %}


## ISS Pass Times

The API returns a list of upcoming ISS passes for a particular location formatted
as JSON.


**Documentation: [ISS Pass Predictions](ISS-Pass-Times)**


## Number of People In Space

**Documentation: [Number of People In Space](People-In-Space)**
