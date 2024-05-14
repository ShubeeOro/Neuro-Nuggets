from flask import Flask, redirect, url_for
# Need to connect MongoDB instead
from neuro_nuggets.models import User, Question
from pathlib import Path 
from flask_login import LoginManager, login_required
from flask_socketio import SocketIO, send, emit
from api.db import db
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

load_dotenv()

# Routes
from api.routes.auth import auth
from api.routes.play import play
from api.routes.main import main

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(play, url_prefix="/play")
    
    return app

app = create_app()

app.config['SECRET_KEY'] = 'space-capybara'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URL")

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

def load_random_question():
    with app.app_context():
        stmt = db.select(Question).order_by(func.random()).limit(1)
        result = db.session.execute(stmt).scalar()

    result.init_answers()
    return result

socketio = SocketIO(app)

# current_question = load_random_question()
score = 1

@socketio.on('connect')
def handle_connect():
    print("COM")
    global game
    game = True
    emit('question', current_question.convert_question())


@socketio.on('timer')
def end_game():
    emit('redirect', "localhost:8888")
        
@socketio.on('my event')
def test_connect_res(data):
    print("RES")
    global current_question
    global score
    print(data)
    if game:
        if current_question.answer_id == int(data):
            current_question = load_random_question()
            emit('question', current_question.convert_question())
            score = score + 1
            emit('score', score)
            print(f"Current Score is {score}")
        else:
            current_question = load_random_question()
            emit('question', current_question.convert_question())
            emit('score', score)
            print(f"Current Score is {score}")

