Applying Varied Artificial Intelligence Techniques to Play 2048
====

**Zhiyang He, Charles Lu, Stephen Ou**

*CS 221 at Stanford University with Percy Liang, Autumn 2015*

Overview
---
We explore various techniques to play 2048: 

1. Randomized and pure strategies
2. Search strategies, i.e. expectimax and minimax
3. Reflex strategies, i.e. regression and neural networks
4. Reinforcement strategies, i.e. Q-learning

Setup
----
To run the front end:

1. Install Flask using `pip install Flask`
2. In the main directory, run `python app.py`, then navigate to `localhost:5000`

Files
-----
* `gameState.py`: provides an abstraction for the 2048 game
* `agents.py`: contains logic behind each of our AI agents
* `play.py`: backend only simulation entry point
* `eval.py`: implements various evaluation functions to score game board
* `data.py`: methods to read and write raw board and move label data for reflex model training
* `tests.py`: unit tests for the 2048 game state and evaluation functions
* `util.py`: miscellanous utility functions
* `reflex.py`: Theano script to train various reflex models
* `appQ.py`: Flask server used to connect Q-learning agents
* `gameStateQ.lua`: the Lua training script that `appQ.py` connects
* `gameStateQ.py`: backend-only Q-learning, does the same thing as appQ.py without frontend
* `gameStateQInit.lua`: Lua script used to reset local data files
* `deepqlearn.{lua,moon}`: DeepQLearning framework by blakeMilner
* `app.py`: the main entry point for Flask (a Python framework), used to connect search agents
* `templates/index.html`: homepage for the 2048 game frontend
* `statics/*.js`: logic for the 2048 game (forked from the original 2048 game by Gabriele Cirulli)


