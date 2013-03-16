import os
from functools import wraps
from flask import Flask, jsonify, request, current_app, render_template, send_from_directory
import iss
import util

app = Flask(__name__)

# json endpoint decorator
def json(func):
    """Returning a object gets JSONified"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs)[0]), func(*args, **kwargs)[1]
    return decorated_function

# from farazdagi on github
#   https://gist.github.com/1089923
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs)[0].data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype), func(*args, **kwargs)[1]
        else:
            return func(*args, **kwargs)
    return decorated_function

# APIs:
API_DEFS = [  {
                "title": "ISS Location Now",
                "link": "/iss-now.json",
                "desc": "Current ISS location over Earth (latitude/longitude)",
                "doclink": "http://open-notify.org/api-doc#iss-now",
                "docname": "api-doc#iss-now"
              },
              {
                "title": "ISS Pass Times",
                "link": "/iss-pass.json",
                "desc": "Predictions when the space station will fly over a particular location",
                "doclink": "http://open-notify.org/api-doc#iss",
                "docname": "api-doc#iss"
              },
              {
                "title": "People in Space Right Now",
                "link": "/astros.json",
                "desc": "The number of people in space at this moment. List of names when known.",
                "doclink": "#",
                "docname": "&ndash;"
              },
           ]

@app.route("/")
def index():
    return render_template('index.html', apis=API_DEFS)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/iss-now.json")
@jsonp
@json
def iss_now():
    loc = iss.get_location()
    return {"message": "success", "data": loc}, 200

@app.route("/iss-pass.json")
@jsonp
@json
def iss_pass():

    # Sanitize inputs
    lat = request.args.get('lat', False)
    if lat:
        lat = util.safe_float(lat, (-90.0,90.0))
        if not lat:
            return {"message": "failure", "reason": "Latitude must be number between -90.0 and 90.0"}, 400
    else:
        return {"message": "failure", "reason": "Latitude must be specified"}, 400

    lon = request.args.get('lon', False)
    if lon:
        lon = util.safe_float(lon, (-180.0,180.0))
        if not lon:
            return {"message": "failure", "reason": "Longitue must be number between -180.0 and 180.0"}, 400
    else:
        return {"message": "failure", "reason": "Longitude must be specified"}, 400

    alt = request.args.get('alt', False)
    if alt:
        alt = util.safe_float(alt, (0,10000))
        if not alt:
            return {"message": "failure", "reason": "Altitude must be number between 0 and 10,000"}, 400
    else:
        return {"message": "failure", "reason": "Altitude must be specified"}, 400

    n = request.args.get('n', False)
    if n:
        n = util.safe_float(n, (1,100))
        if not n:
            return {"message": "failure", "reason": "Number of passes must be number between 1 and 100"}, 400
    else:
        n = 5

    # Calculate data and return
    d = iss.get_passes(lon, lat, alt, int(n))
    return {"message": "success", "data": d}, 200


@app.route("/astros.json")
@jsonp
@json
def astros():
    Astros  = [
        {'name': "Roman Romanenko",   'craft': "ISS"},
        {'name': "Thomas Marshburn",  'craft': "ISS"},
        {'name': "Chris Hadfield",    'craft': "ISS"},
    ] 
    return {'message': "success", 'number': len(Astros), 'people': Astros}, 200

if __name__ == "__main__":
    app.run()
