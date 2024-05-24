import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from api.models import db, User, Question
from sqlalchemy.sql import func
from dotenv import load_dotenv
from datetime import timedelta
import os

from helper import valid_password

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# Routes
from routes.auth import auth
from routes.play import play
from routes.main import main

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 60,
    'pool_pre_ping': True
}

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
    
# Initialize Database
db.init_app(app)

# Blueprints
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(main, url_prefix="/")
app.register_blueprint(play, url_prefix="/play")
    
# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
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



@socketio.on('connect')
def handle_connect():
    print("Connected")
    current_question = load_random_question()
    emit('question', current_question.convert_question())
        
@socketio.on('my event')
def test_connect_res(data):
    print(data)
    if int(data['id'] ) == int(data['user']):
        emit('score', 1)
        current_question = load_random_question()
        emit('question', current_question.convert_question())
    else:
        current_question = load_random_question()
        emit('question', current_question.convert_question())

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)
