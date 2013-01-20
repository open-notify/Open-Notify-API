from flask import Flask, jsonify,bv render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/iss.json")
def iss():
    data = {"hello": "world"}
    resp = jsonify(data)
    print resp
    return resp

if __name__ == "__main__":
    app.run()

