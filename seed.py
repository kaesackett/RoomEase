from model import User, House, Bill, connect_to_db, db
from server import app

def load_users():
    """Load users from users.txt into database."""
    the_file = open("./seed_data/users.txt")
    for line in the_file:
        split_line = line.split("|")
        user_id = split_line[0]
        name = split_line[1]
        house_id = split_line[2]
        phone = split_line[3]
        new_user = User(user_id=user_id, name=name, house_id=house_id, phone=phone)
        db.session.add(new_user)
    db.session.commit()

def load_houses():
    """Load houses from houses.txt into database."""
    the_file = open("./seed_data/houses.txt")
    for line in the_file:
        split_line = line.split("|")
        house_id = split_line[0]
        address = split_line[1]
        new_house = House(house_id=house_id, address=address)
        db.session.add(new_house)
    db.session.commit()

def load_bills():
    """Load bills from bills.txt into database."""
    the_file = open("./seed_data/bills.txt")
    for line in the_file:
        split_line = line.split("|")
        bill_id = split_line[0]
        house_id = split_line[1]
    	due_date = split_line[2]
    	amount = split_line[3]
    	description = split_line[4]
        new_bill = Bill(bill_id=bill_id, house_id=house_id, due_date=due_date, amount=amount, description=description)
        db.session.add(new_bill)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()