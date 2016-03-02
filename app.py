import os
from flask import Flask, request, render_template, send_from_directory
import iss
from util import safe_float, json, jsonp

app = Flask(__name__)

# APIs:
API_DEFS = [
    {
        "title": "ISS Location Now",
        "link": "/iss-now.json",
        "desc": "Current ISS location over Earth (latitude/longitude)",
        "doclink": "http://open-notify.org/Open-Notify-API/ISS-Location-Now",
        "docname": "ISS-Location-Now"},
    {
        "title": "ISS Pass Times",
        "link": "/iss-pass.json?lat=45.0&lon=-122.3",
        "desc": "Predictions when the space station will fly over a particular location",
        "doclink": "http://open-notify.org/Open-Notify-API/ISS-Pass-Times",
        "docname": "ISS-Pass-Times"},
    {
        "title": "People in Space Right Now",
        "link": "/astros.json",
        "desc": "The number of people in space at this moment. List of names when known.",
        "doclink": "http://open-notify.org/Open-Notify-API/People-In-Space",
        "docname": "People-In-Space"},
]


@app.route("/")
def index():
    return render_template('index.html', apis=API_DEFS)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


################################################################################
# Current ISS Location
################################################################################
@app.route("/iss-now.json")
@app.route("/iss-now/")
@app.route("/iss-now/v1/")
@jsonp
@json
def iss_now():
    """The International Space Station (ISS) is moving at close to 28,000 km/h so its
    location changes really fast! Where is it right now?

    This is a simple api to return the current location above the Earth of the ISS.
    It returns the current latitude and longitude of the space station with a unix
    timestamp for the time the location was valid. This API takes no inputs.

    :status 200: when successful

    :>json str message: Operation status.
    :>json int timestamp: Unix timestamp for this location.
    :>json obj iss_position: Position on Earth directly below the ISS.
    :>json int iss_position.latitude: Latitude
    :>json int iss_position.longitude: Longitude

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
        
        {
          "iss_position": {
            "latitude": -19.783929798887073,
            "longitude": -72.29753187401747
          },
          "message": "success",
          "timestamp": 1454357342
        }

    """
    loc = iss.get_location()
    return dict({'message': "success"}, **loc), 200


################################################################################
# ISS Orbit Debug
################################################################################
@app.route("/iss-tle-info.json")
@jsonp
@json
def tle_info():
    info = {'tle': iss.get_tle()}
    info['tle-time'] = iss.get_tle_time()
    info['tle-update'] = iss.get_tle_update()
    return dict({'message': "success"}, **info), 200


################################################################################
# ISS Pass Predictions
################################################################################
@app.route("/iss-pass.json")
@app.route("/iss/")
@app.route("/iss/v1/")
@jsonp
@json
def iss_pass():
    """The international space station (ISS) is an orbital outpost circling
    high above out heads. Sometimes it's overhead, but when? It depends on your
    location. Given a location on Earth (latitude, longitude, and altitude)
    this API will compute the next n number of times that the ISS will be
    overhead.

    Overhead is defined as 10 degrees in elevation for the observer. The times
    are computed in UTC and the length of time that the ISS is above 10 degrees
    is in seconds.

    This gives you enough information to compute pass times for up to several
    weeks, but beware! times are less and less accurate as you go into the future.
    This is because the orbit of the ISS decays unpredictably over time and because
    station controllers periodically move the station to higher and lower orbits
    for docking, re-boost, and debris avoidance.

    **Overview**

    The API returns a list of upcoming ISS passes for a particular location
    formatted as JSON.

    As input it expects a latitude/longitude pair, altitude and how many results
    to return. All fields are required.

    As output you get the same inputs back (for checking) and a time stamp when
    the API ran in addition to a success or failure message and a list of passes.
    Each pass has a duration in seconds and a rise time as a unix time stamp.

    :status 200: when successful
    :status 400: if one or more inputs is out of range or invalid

    :query lat: latitude in decimal degrees of the ground station. **required** Range: -90, 90
    :query lon: longitude in decimal degress of the ground station. **required** Range: -180, 180
    :query alt: altitude in meters of the gronud station. optional. Range: 0, 10,000
    :query n: requested number of predictions. default: 5. May return less than requested

    :>json str message: Operation status.
    :>json obj request: Parameters used in prediction
    :>json list response: List of predicted passes

    **Example Request**:

    .. sourcecode:: http

        GET /iss/v1/?lat=40.027435&lon=-105.251945&alt=1650&n=1 HTTP/1.1
        Host: api.open-notify.org
        Accept: application/json, text/javascript


    **Example Response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "message": "success",
          "request": {
            "altitude": 1650.0,
            "datetime": 1454475126,
            "latitude": 40.027435,
            "longitude": -105.251945,
            "passes": 1
          },
          "response": [
            {
              "duration": 525,
              "risetime": 1454475538
            }
          ]
        }

    """

    # Sanitize inputs
    lat = request.args.get('lat', False)
    if lat:
        lat = safe_float(lat, (-90.0, 90.0))
        if not lat:
            return {"message": "failure", "reason": "Latitude must be number between -90.0 and 90.0"}, 400
    else:
        return {"message": "failure", "reason": "Latitude must be specified"}, 400

    lon = request.args.get('lon', False)
    if lon:
        lon = safe_float(lon, (-180.0, 180.0))
        if not lon:
            return {"message": "failure", "reason": "Longitue must be number between -180.0 and 180.0"}, 400
    else:
        return {"message": "failure", "reason": "Longitude must be specified"}, 400

    alt = request.args.get('alt', False)
    if alt:
        alt = safe_float(alt, (0, 10000))
        if not alt:
            return {"message": "failure", "reason": "Altitude must be number between 0 and 10,000"}, 400
    else:
        alt = 100

    n = request.args.get('n', False)
    if n:
        n = safe_float(n, (1, 100))
        if not n:
            return {"message": "failure", "reason": "Number of passes must be number between 1 and 100"}, 400
    else:
        n = 5

    # Calculate data and return
    d = iss.get_passes(lon, lat, alt, int(n))
    return dict({"message": "success"}, **d), 200


################################################################################
# Current People In Space
################################################################################
@app.route("/astros.json")
@app.route("/astros/")
@app.route("/astros/v1/")
@jsonp
@json
def astros():
    Astros = [
        {'name': "Yuri Malenchenko",        'craft': "ISS"},
        {'name': "Timothy Kopra",           'craft': "ISS"},
        {'name': "Timothy Peake",           'craft': "ISS"},
    ]
    return {'message': "success", 'number': len(Astros), 'people': Astros}, 200


if __name__ == "__main__":
    app.debug = True
    app.run()
