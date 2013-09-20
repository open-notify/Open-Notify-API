---
layout: apidoc
name: astros
title: Open Notify -- API Doc | People In Space Now
---

# How Many People Are In Space Right Now

<http://api.open-notify.org/astros.json>

How many humans are in space _right now_?


## Overview

This API returns the current number of people in space. When known it also
returns the names and spacecraft those people are on. This API takes no inputs.


## Output

### JSON

<http://api.open-notify.org/astros.json>

{% highlight javascript %}
{
  "message": "success",
  "number": NUMBER_OF_PEOPLE_IN_SPACE,
  "people": [
    {"name": NAME, "craft": SPACECRAFT_NAME},
    ...
  ]
}
{% endhighlight %}

### JSONP

Appending a callback request to the query string will return JSONP:

<http://api.open-notify.org/astros.json?callback=CALLBACK>

{% highlight javascript %}
CALLBACK({
  "message": "success",
  "number": %NUMBER_OF_PEOPLE_IN_SPACE%,
  "people": [
    {"name": %NAME%, "craft": %SPACECRAFT_NAME%},
    ...
  ]
})
{% endhighlight %}


## Examples

Here is an example using jquery:

{% highlight javascript %}
$.getJSON('http://api.open-notify.org/astros.json', function(data) {
  console.log(data['number'])
});
{% endhighlight %}

This should log the number of people in space to the console.


## Data Source

I gather and update this data personally as launches and landing occur.
There is no official source of data for this kind of thing.
