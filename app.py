from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import time
import random
import json
app = Flask(__name__)

@app.route("/")
def display():
	return render_template('index.html')

@app.route("/move")
def move():
	# Plug in the algorithm below
	# 0: Up, 1: Right, 2: Down, 3: Left
	data = {
        'move'  : random.randint(0, 3),
    }
	js = json.dumps(data)
	# Plug in the algorithm above

	layout = json.loads(request.args.get('layout'))
	print layout["score"]
	print layout["grid"]
	time.sleep(3)

	resp = Response(js, status=200, mimetype='application/json')
	return resp

if __name__ == "__main__":
    app.run()
