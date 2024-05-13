import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import re
from unittest.mock import patch

import pytest
from werkzeug.security import generate_password_hash, check_password_hash

from neuro_nuggets.models import User
from neuro_nuggets.db import db
from neuro_nuggets.app import app

@pytest.fixture
def user_dummy():
    password = "password"
    email = "test@email.com"
    name = "Test"

    # Create user fixture in database if it doesn't exist
    with app.app_context():
        find_user = db.session.query(User).filter_by(email=email).first()
        if not find_user:
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(password, method='scrypt'),
            )
            db.session.add(user)
            db.session.commit()

    return password, email, name

def test_create_user(user_dummy):
    [password,email,name] = user_dummy

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method='scrypt'),
    )

    assert check_password_hash(user.password, password)
    assert user.email == "test@email.com"
    assert user.name == "Test"

def test_create_user_extra():
    password = "password"
    email = "email@email.com"
    name = "Bob"

    with app.app_context():
        find_user = db.session.query(User).filter_by(email=email).first()
        if find_user:
            db.session.delete(find_user)
            db.session.commit()

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='scrypt'),
        )

        assert check_password_hash(user.password, password)
        assert user.email == "email@email.com"
        assert user.name == "Bob"

        db.session.add(user)
        db.session.commit()
        find_user = db.session.query(User).filter_by(email=email).first()

        assert type(find_user.id) == int
        assert check_password_hash(find_user.password, password)
        assert find_user.email == "email@email.com"
        assert find_user.name == "Bob"

        db.session.delete(find_user)
        db.session.commit()


def test_existing_user(user_dummy):
    [password,email,name] = user_dummy

    with app.app_context():
        user = db.session.query(User).filter_by(email=email).first()
    assert user.email == email
    assert user.name == name
    assert isinstance(user.password, str)
    assert user.password[:6] == "scrypt"
    assert check_password_hash(user.password, password)

def test_user_highscore_default(user_dummy):
    [password,email,name] = user_dummy

    with app.app_context():
        user = db.session.query(User).filter_by(email=email).first()

    assert type(user.highscore) == int
    assert user.highscore == 0
    
    user.highscore = 100
    assert user.highscore == 100
    