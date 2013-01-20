from flask import Flask, jsonify, render_template
import iss
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/iss-now.json")
def iss_now():
    loc = iss.get_location()
    return jsonify({"message": "success", "data": loc})

if __name__ == "__main__":
    app.run()
