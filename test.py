import datetime
import unittest
import tempfile
import json
import os
import flask

from model import User, House, Bill, User_Payment
from server import app, db
import seed

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.db_filename
        app.config['TESTING'] = True
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.test_client = app.test_client()
        db.app = app
        db.init_app(app)
        with app.app_context():
            db.create_all()
        seed.load_users()
        seed.load_houses()

    def login(self, client):
        return client.post('/login_handler', data=dict(
                email="kae@gmail.com",
                password="actualpassword"
                ), follow_redirects=True)

    def test_login(self):
        """Checks that a user is in session after login with correct credentials."""
        with app.test_client() as c:
            self.login(c)
            assert flask.session['email'] == "kae@gmail.com"

    def test_database_seed(self):
        """Ensures that the database seed file is functioning as expected."""

        user = User.query.filter_by(user_id=1).one()
        house = House.query.filter_by(house_id=2).one()
        assert user.email == "kae@gmail.com"
        assert house.address == "410 Forney Ave Jacksonville, AL 36265"

    def test_add_bill(self):
        """Ensures that a bill is created in the database with the correct
        information when a user adds a bill through their account."""

        new_bill = Bill(description="Test Bill", due_date=datetime.date(2016,1,1), amount=45.60, house_id=2)
        db.session.add(new_bill)
        db.session.commit()
        assert Bill.query.filter_by(description="Test Bill").one()

    def test_add_bill_handler(self):
        """Ensures that both a Bill object and a User_Payment object are
        created in the database once the user accesses the Add Bill page."""

        assert len(Bill.query.filter_by(description="Test Bill").all()) == 0
        with app.test_client() as c:
            self.login(c)
            user = User.query.filter_by(email=flask.session["email"]).one()
            c.post('/add_bill_handler', data=dict(
                description="Test Bill",
                due_date="2016-01-01",
                amount="45.60"
                ), follow_redirects=True)
            
        assert Bill.query.filter_by(description="Test Bill").one()
        assert User_Payment.query.filter_by(user_id=user.user_id).one()

    def test_empty_db(self):
        """Tests that a user would receive a 404 error
        when trying to access a nonexistant route."""

        response = self.test_client.get('/SOMENONEXISTANTPLACE')
        assert response.status_code == 404

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)


if __name__ == '__main__':
    unittest.main()