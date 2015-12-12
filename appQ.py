from subprocess import Popen, PIPE, STDOUT
from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import time
import random
import json
import sys
app = Flask(__name__)

last_score = 0
ind = 0
p = Popen(['th', 'gameStateQ.lua'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
score_record = []
max_score = 0
ave_score = 550
max_grid = 0

## Q Learning Server

@app.route("/")
def display():
	return render_template('index.html')

@app.route("/move", methods=['GET'])
def move():
	global last_score
	global ind
	global f
	global score_record
	global max_score
	global ave_score
	global max_grid
	layout = json.loads(request.args.get('layout'))

	### Book keeping of score
	new_score = layout["score"]
	new_max_grid = getMaxGrid(layout["grid"])
	"""
	if new_score > max_score:
		max_score = new_score
	"""
	if len(score_record) == 16:
		f = open('qlearning/trainingRecord.csv', 'a')
		ave_score = float(sum(score_record))/(len(score_record))
		f.write(str(ave_score) + "\n")
		f.close()
		score_record = []
	new_won = layout["won"]
	reward = 0
	print "record length", len(score_record) 
	
	reward = new_max_grid
	if new_won:
		reward += 100000000
	if new_max_grid > max_grid:
		max_grid = new_max_grid
		reward += 100000000
	if (new_score < last_score):
		score_record.append(last_score)
		# f.write(str(last_score) + "\n")
		if not new_won:
			reward = -ave_score
			# reward = -100000
	"""
	else:
		if not new_won:
			# reward = (new_score - last_score)**2
			reward = new_score
		if reward == 0:
			reward = -50
	"""
	last_score = layout["score"]
	
	### Input to lua process
	layoutStr = gridToStr(layout['grid'], reward)
	# print "input", layoutStr
	p.stdin.write(layoutStr)

	qOutput = p.stdout.readline()
	# print "output", qOutput
	print "index", str(ind)

	### Feed move into front-end
	data = {'move': int(qOutput),} 			# 0: Up, 1: Right, 2: Down, 3: Left
	resp = Response(json.dumps(data), status=200, mimetype='application/json')

	# Keep track of number of moves
	ind += 1
	return resp

def gridToStr(layout, reward):
	global max_score
	gridStr = ""
	for row in layout:
		for num in row:
			gridStr += str(num) + " "
	return gridStr + str(reward) + " " +  str(max_score) + " \n"

def getMaxGrid(layout):
	maxGrid = 0
	for row in layout:
		for grid in row:
			if grid > maxGrid:
				maxGrid = grid
	return maxGrid

if __name__ == "__main__":
    app.run(debug=True)
