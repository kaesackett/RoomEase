"""RoomEase organization application, Flask server.

Provides web interface for organizing tasks between roommates.
Includes bill division and reminders, group calendar, and 
other useful stuff. 

Author: Kaelyn Sackett for Hackbright Academy, Summer 2015
"""

import datetime
import jinja2
import os
from utils import send_text_reminder
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from model import User, House, Bill, User_Payment, Message, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
from twilio.rest import TwilioRestClient

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
    
    if session.get("email"):
        send_text_reminder(session["email"], client)
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

@app.route("/calendar/events")
def create_events():
    """Queries the database for due dates of unpaid bills and creates calendar events for them."""

    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id
    house_bills = Bill.query.filter_by(house_id=house_id, paid=False).all()
    bills_dict = {}
    for bill in house_bills:
        bills_dict[bill.description] = datetime.datetime.strftime(bill.due_date, "%Y-%m-%d")
    return jsonify(bills_dict)

@app.route("/bills")
def bill_list():
    """Show list of bills."""

    if session:
        user = User.query.filter_by(email=session["email"]).one()
        house_id = user.house_id
        house_bills = Bill.query.filter_by(house_id=house_id, paid=False).all()
        bills = User_Payment.query.filter_by(user_id=user.user_id, paid=False).all()
        for bill in bills:
            bill2 = Bill.query.filter_by(bill_id=bill.bill_id).one()
            bill.description = bill2.description
            bill.due_date = bill2.due_date
        count = User.query.filter_by(house_id=house_id).count()
        return render_template("bill_list.html", bills=bills, house_bills=house_bills, count=count)
    else:
        return render_template("nope.html")

@app.route("/add_bill")
def show_add_bill_page():
    """Show user the form used to enter a new bill into the database."""

    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id
    bills = Bill.query.filter_by(house_id=house_id).all()
    return render_template("add_bill.html")

@app.route("/add_bill_handler")
def add_bill():
    """Insert a new bill into the database."""

    description = request.args.get("description")
    due_date = datetime.datetime.strptime(request.args.get("due_date"), "%Y-%m-%d")
    amount = request.args.get("amount")
    # Get house_id from the user in session
    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id

    new_bill = Bill(description=description, due_date=due_date, amount=amount, house_id=house_id)
    db.session.add(new_bill)
    db.session.commit()
    for user in User.query.filter_by(house_id=house_id).all():
        new_user_payment = User_Payment(amount=amount, user_id=user.user_id, bill_id=new_bill.bill_id)
        db.session.add(new_user_payment)
    db.session.commit()
    return redirect('/bills')

@app.route("/edit_bills")
def show_edit_bill_page():
    """Show the user the form used to delete bills from the database by indicating that they have been paid."""

    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id
    bills = User_Payment.query.filter_by(user_id=user.user_id).all()
    for bill in bills:
        bill2 = Bill.query.filter_by(bill_id=bill.bill_id).one()
        bill.description = bill2.description
        bill.due_date = bill2.due_date
    count = User.query.filter_by(house_id=house_id).count()
    return render_template("edit_bills.html", bills=bills, count=count)

@app.route("/edit_bill_handler")
def edit_bill():
    """Perform the deletion actions initiated by the form submitted in the /edit_bills route."""

    user = User.query.filter_by(email=session["email"]).one()
    bill_id = request.args.get("bill_id")
    user_payment = User_Payment.query.filter_by(user_id=user.user_id, bill_id=bill_id).one()
    user_payment.paid = True
    db.session.commit()
    if not User_Payment.query.filter_by(bill_id=bill_id, paid=False).all():
        bill_to_be_paid = Bill.query.filter_by(bill_id=bill_id).one()
        bill_to_be_paid.paid = True
    db.session.commit()

    return redirect("/bills")

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

@app.route("/message_handler")
def add_message():
    """Gets a message as input from a form on the message board page and 
    commits that message along with relevant sender info to the database."""

    user = User.query.filter_by(email=session["email"]).one()
    house_id = user.house_id
    content = request.args.get('content')
    created_at = datetime.datetime.now()
    new_message = Message(user_id=user_id, content=content, created_at=created_at)
    db.session.add(new_message)
    db.session.commit()

    roommate_ids = []
    roommates = User.query.filter_by(house_id=house_id).all()
    for roommate in roommates:
        roommate_ids.append(roommate.user_id)
    house_messages = Message.query.filter(user_id in roommate_ids).all()
    return house_messages

@app.route("/my_profile")
def my_profile():
    """Show details of the account of the user currently in session."""

    if session:
        user = User.query.filter_by(email=session["email"]).one()
        return render_template("my_profile.html")
    else:
        return render_template("nope.html")

if __name__ == "__main__":
    # app.debug = True
    # # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()