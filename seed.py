from model import User, House, Bill, User_Payment, connect_to_db, db
from server import app

def load_users():
    """Load users from users.txt into database."""
    the_file = open("./seed_data/users.txt")
    for line in the_file:
        split_line = line.split("|")
        user_id = split_line[0]
        email = split_line[1]
        password = split_line[2]
        name = split_line[3]
        house_id = split_line[4]
        phone = split_line[5]
        new_user = User(email=email, password=password, name=name, house_id=house_id, phone=phone)
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

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_houses()