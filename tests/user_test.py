import logging

from flask_login import current_user

from app import db
from app.db.models import User, Transaction
from faker import Faker


def test_adding_user(application):
    """This test adding a new user"""
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        # showing how to add a record
        # create a record
        user = User('sd84@njit.edu', 'sd84')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        db.session.commit()
        # assert that we now have a new user
        assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='sd84@njit.edu').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'sd84@njit.edu'
        # this is how you get a related record ready for insert
        user.transactions = [Transaction("1", "200", "CREDIT"), Transaction("2", "-200", "DEBIT")]
        # commit is what saves the transactions
        db.session.commit()
        assert db.session.query(Transaction).count() == 2
        transaction1 = Transaction.query.filter_by(transaction_type='CREDIT').first()
        assert transaction1.transaction_type == "CREDIT"
        # changing the title of the song
        transaction1.transaction_type = "DEBIT"
        # saving the new title of the song
        db.session.commit()
        transaction2 = Transaction.query.filter_by(transaction_type='DEBIT').first()
        assert transaction2.transaction_type == "DEBIT"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0


def test_edit_user_profile(client):
    """This tests editing user profile"""
    with client:
        register_response = client.post("/register", data={
            "email": "sd84@njit.edu",
            "password": "NJITmother@1",
            "confirm": "NJITmother@1"
        },
                                        follow_redirects=True)
        login_response = client.post("/login", data={
            "email": "sd84@njit.edu",
            "password": "NJITmother@1"
        },
                                     follow_redirects=True)

        assert login_response.status_code == 400

        form_data = {
            "about":  f"Hi! i am sd84"
        }

        user_update_response = client.post(
            "/profile",
            data=form_data,
            follow_redirects=True)

        user_object = User.query.filter_by(email='sd84@njit.edu').first()

        assert user_update_response.status_code == 400


def test_edit_user_account(client):
    """This tests editing user account"""
    with client:
        register_response = client.post("/register", data={
            "email": "sd84@njit.edu",
            "password": "NJITmother@1",
            "confirm": "NJITmother@1"
        },
                                        follow_redirects=True)
        login_response = client.post("/login", data={
            "email": "testuser1@test.com",
            "password": "NJITmother@1"
        },
                                     follow_redirects=True)
        assert login_response.status_code == 400

        form_data = {
            "email":  f"sd85@njit.edu",
            "password": f"NJITmother@1",
            "confirm": f"NJITmother@1"
        }

        user_update_response = client.post(
            "/account",
            data=form_data,
            follow_redirects=True)

        assert user_update_response.status_code == 400
