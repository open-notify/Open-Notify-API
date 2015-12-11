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
        {'name': "Mikhail Kornienko",       'craft': "ISS"},
        {'name': "Scott Kelly",             'craft': "ISS"},
        {'name': "Sergey Volkov",           'craft': "ISS"},
    ]
    return {'message': "success", 'number': len(Astros), 'people': Astros}, 200


if __name__ == "__main__":
    app.debug = True
    app.run()
