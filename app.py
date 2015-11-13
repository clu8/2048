from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import time
import random
import json
import gameState
app = Flask(__name__)

@app.route("/")
def display():
	return render_template('index.html')

@app.route("/move")
def move():
	layout = json.loads(request.args.get('layout'))
	data = {'move': gameState.run(layout["grid"], layout["score"]),}
	time.sleep(0.1)
	resp = Response(json.dumps(data), status=200, mimetype='application/json')
	return resp

if __name__ == "__main__":
    app.run(debug=True)
