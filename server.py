"""RoomEase organization application, Flask server.

Provides web interface for organizing tasks between roommates.
Incl bill division and reminders, group calendar, message board,
and other useful stuff. 

Author: Kaelyn Sackett for Hackbright Academy, Summer 2015
"""

from flask import Flask, request, render_template, redirect, flash, session
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from model import User, House, Bill, connect_to_db, db

app = Flask(__name__)

app.secret_key = 'TX24653346kns!2015'

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/", methods=["GET", "POST"])
def index():
	"""Return homepage."""
	return render_template("index.html")

@app.route("/sign_up")
def show_signup_page():
    """Allow the user access to the form that they can use to register for my site."""
    return render_template("sign_up.html")

@app.route('/sign_up_handler', methods=["POST"])
def handle_signup():
    """Process sign up info to create a new user in the database."""

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")

    try:
        house = House.query.filter(House.address==address).one()
    except:
        new_house = House(address=address)
        db.session.add(new_house)
        db.session.commit()
        house = House.query.filter(House.address==address).one()
    house_id = house.house_id
    new_user = User(email=email, password=password, name=name, phone=phone, house_id=house_id)
    print new_user
    db.session.add(new_user)
    db.session.commit()
    flash("Welcome new user!")
    session["email"] = email
    return redirect('/')

@app.route('/login_handler', methods=["POST"])
def handle_login():
    """Process login info."""

    email = request.form.get("email")
    password = request.form.get("password")

    #If both email and password are correct, log them in
    if User.query.filter(User.email == email, User.password == password).first():
        flash("You are now logged in.")
        session["email"] = email
        return redirect('/')
    #if email is correct but not password, tell them they fucked up
    elif User.query.filter(User.email == email, User.password != password).first(): 
        flash("Incorrect login information provided. Please try again.")
        return redirect("/")

@app.route('/logout', methods=["POST"])
def handle_logout():
    """Process user logout."""

    del session["email"]
    flash("You are now logged out.")
    return redirect('/')

@app.route("/calendar")
def show_calendar():
    """Show the user the group calendar for their house."""

    if session:
        return render_template("calendar.html")
    else:
        return render_template("nope.html")

@app.route("/bills")
def bill_list():
    """Show list of bills."""

    if session:
        user = User.query.filter_by(email=session["email"]).one()
        house_id = user.house_id
        bills = Bill.query.filter_by(house_id=house_id).all()
        print bills
        return render_template("bill_list.html", bills=bills)
    else:
        return render_template("nope.html")

@app.route("/roomies")
def roomie_list():
    """Show list of roommates."""

    if session:
        user = User.query.filter_by(email=session["email"]).one()
        house_id = user.house_id
        roommates = User.query.filter_by(house_id=house_id).all()
        return render_template("roomie_list.html", roommates=roommates)
    else:
        return render_template("nope.html")

@app.route("/my_profile")
def my_profile():
    """Show details of the account of the user currently in session."""

    if session:
        user = User.query.filter_by(email=session["email"]).one()
        return render_template("my_profile.html")
    else:
        return render_template("nope.html")

if __name__ == "__main__":
    app.debug = True
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()