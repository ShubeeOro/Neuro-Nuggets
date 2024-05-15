from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from db import db
from models import User
import re

auth = Blueprint('auth', __name__)

def valid_password(password:str) -> bool:
    flag = False
    if not isinstance(password, str):
        raise ValueError
    while True:
        if (len(password)<=8):
            flag = True
            break
        elif not re.search("[a-z]", password):
            flag = True
            break
        elif not re.search("[A-Z]", password):
            flag = True
            break
        elif not re.search("[0-9]", password):
            flag = True
            break
        elif not re.search("[_@$]" , password):
            flag = True
            break
        elif re.search("\s" , password):
            flag = True
            break
        else:
            break
    
    if flag:
        return False
    else:
        return True


@auth.route('/login')
def login():
    return render_template('pages/login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    email: str
    password: str
    remember: bool

    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.session.query(User).filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('pages/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email: str
    password: str
    name: str

    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = db.session.query(User).filter_by(email=email).first()

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Successful Signup! Please Login')
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))