"""RoomEase organization application, Flask server.

Provides web interface for organizing tasks between roommates.
Includes bill division and reminders, group calendar, and 
other useful stuff. 

Author: Kaelyn Sackett for Hackbright Academy, Summer 2015
"""

import jinja2
import os
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.rest import TwilioRestClient
from model import User, House, Bill, connect_to_db, db

app = Flask(__name__)

app.secret_key = 'TX24653346kns!2015'

app.jinja_env.undefined = jinja2.StrictUndefined

# Twilio API Connection and Authorization
account = os.environ['TWILIO_ACCOUNT_SID']
token = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account, token)

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
        return render_template("bill_list.html", bills=bills)
    else:
        return render_template("nope.html")

@app.route("/add_bill")
def show_add_bill_page():
    """Show user the form used to enter a new bill into the database."""

    return render_template("add_bill.html")

@app.route("/add_bill_handler")
def add_bill():
    """Insert a new bill into the database."""

    description = request.args.get("description")
    due_date = request.args.get("due_date")
    amount = request.args.get("amount")
    # Get house_id from the user in session
    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id

    new_bill = Bill(description=description, due_date=due_date, amount=amount, house_id=house_id)
    db.session.add(new_bill)
    db.session.commit()
    return redirect('/bills')

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