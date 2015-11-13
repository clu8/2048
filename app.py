from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import time
import random
import json
import sys
app = Flask(__name__)

record = []
last_score = 0

@app.route("/")
def display():
	return render_template('index.html')

@app.route("/move", methods=['GET'])
def move():
	global record
	global last_score
	# Plug in the algorithm below
	# 0: Up, 1: Right, 2: Down, 3: Left
	data = {
        'move'  : random.randint(0, 3),
    }
	js = json.dumps(data)
	# Plug in the algorithm above

	layout = json.loads(request.args.get('layout'))
	print last_score
	print record
	print layout["score"]
	print layout["grid"]
	if (layout["score"] < last_score):
		if (len(record) > 100):
			print record
			sys.exit(0)
		record.append(last_score)
	last_score = layout["score"]
	# print layout["grid"]
	# time.sleep(0.01)
	resp = Response(js, status=200, mimetype='application/json')
	# print "a"
	return resp

if __name__ == "__main__":
    app.run()
