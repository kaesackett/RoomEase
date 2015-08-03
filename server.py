"""RoomEase organization application, Flask server.

Provides web interface for organizing tasks between roommates.
Incl bill division and reminders, group calendar, message board,
and other useful stuff. 

Author: Kaelyn Sackett for Hackbright Academy, Summer 2015
"""

from flask import Flask, request, render_template, redirect, flash
import jinja2
from model import User, House, Bill, connect_to_db, db

app = Flask(__name__)

app.secret_key = 'TX24653346kns!2015'

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/", methods=["GET", "POST"])
def index():
	"""Return homepage."""
	return render_template("index.html")

@app.route('/login_handler', methods=["POST"])
def handle_login():
    """Process login info."""

    email = request.form.get("email")
    password = request.form.get("password")

    #If both email and password are correct, log them in
    if User.query.filter(User.email == email, User.password == password).first():
        flash("You are now logged in.")
        session["email"] = email
    #if email is correct but not password, tell them they fucked up
    elif User.query.filter(User.email == email, User.password != password).first(): 
        flash("Incorrect login information provided. Please try again.")
        return redirect("/login_form")
    #If both email and pass were incorrect, make a new user
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Welcome new user. You've been added to our database!")
        session["email"] = email
    return redirect('/')

@app.route('/logout', methods=["POST"])
def handle_logout():
    """Process user logout."""

    del session["email"]
    flash("You are now logged out.")
    return redirect('/')

@app.route("/calendar")
def show_calendar():
    """Show the user the group calendar for their house."""

    # STUFF IN HERE
    return render_template("calendar.html")

@app.route("/bills")
def bill_list():
    """Show list of bills."""

    # ....
    # bills = Bill.query.order_by(bill.description).all()
    return render_template("bill_list.html")

@app.route("/roomies")
def roomie_list():
    """Show list of roommates."""

    # ....
    return render_template("roomie_list.html")

@app.route("/my_profile")
def my_profile():
    """Show details of the account of the user currently in session."""

    # QUERY FOR USER AND STUFF HERE
    return render_template("my_profile.html")

if __name__ == "__main__":
    app.run(debug=True)