from flask import Flask
from flask import render_template
from flask import Response
import time
import random
import json
app = Flask(__name__)

@app.route("/")
def display():
	return render_template('index.html')

@app.route("/move", methods=['GET'])
def move():
	data = {
        'move'  : random.randint(0, 3),
    }
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	time.sleep(0.2)
	return resp

if __name__ == "__main__":
    app.run()
