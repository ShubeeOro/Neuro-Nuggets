from flask import Flask, url_for, request, flash
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask_socketio import SocketIO, send, emit
from models import db, User, Question
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

from helper import valid_password

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# Routes
from routes.auth import auth
from routes.play import play
from routes.main import main

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')
    
# Initialize Database
db.init_app(app)

# Blueprints
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(main, url_prefix="/")
app.register_blueprint(play, url_prefix="/play")
    
# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Socket IO
socketio = SocketIO(app)

def load_random_question():
    with app.app_context():
        stmt = db.select(Question).order_by(func.random()).limit(1)
        result = db.session.execute(stmt).scalar()

    result.init_answers()
    return result

current_question = load_random_question()
score = 0

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
    print(data)
    if game:
        if current_question.answer_id == int(data):
            current_question = load_random_question()
            emit('question', current_question.convert_question())
            emit('score', 1)
        else:
            current_question = load_random_question()
            emit('question', current_question.convert_question())
            emit('score', 0)

