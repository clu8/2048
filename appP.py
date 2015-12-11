## Auxiliary q learning server

from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import sys
app = Flask(__name__)


@app.route("/")
def display():
	strA = ""
	with open("training_meta.txt") as f:
		strA = str(f.readlines())
	return strA


if __name__ == "__main__":
    app.run(port=5001)
