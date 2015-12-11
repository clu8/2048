Applying Varied Artificial Intelligence Techniques to Play 2048

CS 221 at Stanford University with Percy Liang, Autumn 2015

Zhiyang He, Charles Lu, Stephen Ou

To run the front end:
	1) Install flask using "pip install Flask"
	2) In the main directory, run "python app.py", then go to localhost:5000

gameState.py: provides an abstraction for the 2048 game
agents.py: contains logic behind each of our 6 agents
eval.py: calculates the score of a game board based on different evaluation functions
data.py: uses to generate human readable data files based on a game board
tests.py: unit tests for the 2048 game state
util.py: miscellanous utility functions
app.py: the main entry point for Flask (a Python framework)
templates/index.html: homepage for the 2048 game frontend
statics/*.js: logic for the 2048 game (borrowed from the original 2048 game by Gabriele Cirulli)
