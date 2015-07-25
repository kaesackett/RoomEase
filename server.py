"""RoomEase organization application, Flask server.

Provides web interface for organizing tasks between roommates.
Incl bill division and reminders, group calendar, message board,
and other useful stuff. 

Author: Kaelyn Sackett for Hackbright Academy, Summer 2015
"""

from flask import Flask, request, render_template, redirect, flash
import jinja2

# import model

app = Flask(__name__)

app.secret_key = 'TX24653346kns!2015'

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
	"""Return homepage."""
	return render_template("index.html")

@app.route("/other-page")
def load_other_page():
	return render_template("other-page.html",
							jinja_stuff = jinja_stuff)

# OTHER ROUTES TO BE ADDED HERE

if __name__ == "__main__":
    app.run(debug=True)