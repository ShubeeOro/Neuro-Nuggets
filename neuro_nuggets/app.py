import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask, redirect, url_for
from neuro_nuggets.models import User, Question
from neuro_nuggets.db import db
from pathlib import Path 
from flask_login import LoginManager, login_required
from flask_socketio import SocketIO, send, emit
from sqlalchemy.sql import func

# Routes
from neuro_nuggets.routes.auth import auth
from neuro_nuggets.routes.play import play
from neuro_nuggets.routes.main import main

app = Flask(__name__)

# Connects the db to the app
app.config['SECRET_KEY'] = 'space-capybara'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
app.instance_path = Path("data/storage.db").resolve()
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Socket IO
socketio = SocketIO(app)

# Blueprints
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(main, url_prefix="/")
app.register_blueprint(play, url_prefix="/play")

def load_random_question():
    with app.app_context():
        stmt = db.select(Question).order_by(func.random()).limit(1)
        result = db.session.execute(stmt).scalar()

    result.init_answers()
    return result

current_question = load_random_question()
score = 1

@socketio.on('connect')
def handle_connect():
    print("COM")
    global game
    game = True
    emit('question', str(current_question))


@socketio.on('timer')
def end_game():
    emit('redirect', "localhost:8888")
        
@socketio.on('my event')
def test_connect_res(data):
    print("RES")
    global current_question
    global score
    if game:
        if current_question.answer_id == int(data):
            current_question = load_random_question()
            emit('question', str(current_question))
            score = score + 1
            emit('score', score)
            print(f"Current Score is {score}")
        else:
            current_question = load_random_question()
            emit('question', str(current_question))
            emit('score', score)
            print(f"Current Score is {score}")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8888)