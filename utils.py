from model import User, Bill, House, User_Payment
from flask import session
import datetime
import os

my_number = os.environ['my_number']

def send_text_reminder(email, client):
    """Check all a house's bills for upcoming due dates. 
    If a bill is due tomorrow and that bill has still not 
    been paid, send a text reminder to the residents in that
    house who have not paid their portion."""

    user = User.query.filter_by(email=email).one()
    house_id = user.house_id
    house_bills = Bill.query.filter_by(house_id=house_id, paid=False).all()
    for bill in house_bills:
        residents_who_havent_paid = find_bill_users_who_havent_paid(bill.bill_id)
        for resident in residents_who_havent_paid:
            if bill.due_date == datetime.date.today() + datetime.timedelta(days=1):
                message = client.messages.create(to=my_number, from_="+12568874445", body="Heads up: Your "+str(bill.description)+" bill is due tomorrow!")

def find_bill_users_who_havent_paid(bill_id):
    user_payments_for_bill = User_Payment.query.filter_by(bill_id=bill_id, paid=False).all()
    users = [user_payment.user for user_payment in user_payments_for_bill]
    return users