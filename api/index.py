from flask import Flask, redirect, url_for, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask_socketio import SocketIO, send, emit
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

from helper import valid_password

from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


app = Flask(__name__)

# Routes
#from api.routes.auth import auth
#from api.routes.play import play
#from api.routes.main import main

# Database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')

# Database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Database Models
from sqlalchemy import ForeignKey, Integer, String, TEXT
from flask_login import UserMixin
from sqlalchemy.orm import mapped_column, relationship
from random import shuffle 
from sqlalchemy.sql import func
import json

class User(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(200), nullable=False, unique=True)
    password = mapped_column(String(200), nullable=False)
    name = mapped_column(String(200), nullable=False)
    highscore = mapped_column(Integer(), nullable=True,default=0)

class Question(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    question = mapped_column(String(200), nullable=False, unique=True)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers = mapped_column(TEXT(400), nullable=False)
    category = mapped_column(String(100), nullable=False)
    difficulty = mapped_column(String(100), nullable=False, default=0)

    # Required to initalize the question from the database
    # When you load a question row from the database, 
    def init_answers(self) -> None:
        # Answer List
        answers = json.loads(self.incorrect_answers)
        answers.append(self.correct_answer)
        shuffle(answers)
        self.answers = answers
        self.answer_id  = answers.index(self.correct_answer) + 1

    def convert_question(self) -> dict:
        if not self.answers:
            self.init_answers()
        
        return {
            "question": self.question,
            "correct_answer": self.correct_answer,
            "answers": self.answers,
            "answer_id": self.answer_id
        }

    def __getitem__(self, index):
        if isinstance(index, str):
            if index == 'question':
                return self.question
            if index == 'correct_answer':
                return self.correct_answer
            if index == 'incorrect_answers':
                return self.incorrect_answers
            if index == 'category':
                return self.category
            if index == 'difficulty':
                return self.difficulty
        
    def __str__(self):
        return_str = f"{self.question}"

        for index, value in enumerate(self.answers):
            return_str += f"\n{index + 1}. {value}"

        return return_str
    
# Initialize Database
db.init_app(app)

# Blueprints
#app.register_blueprint(auth, url_prefix="/")
#app.register_blueprint(main, url_prefix="/")
#app.register_blueprint(play, url_prefix="/play")
    
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

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/play')
@login_required
def start_game():
    return render_template('pages/game_mode.html')

@app.route('/endless')
@login_required
def endless_game():
    return render_template('pages/endless.html')

@app.route('/solo')
@login_required
def solo_game():
    return render_template('pages/solo.html')


# Shows profile
@app.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    if request.method == "POST":
        new_name = request.form["username"]
        if new_name:
            user = db.get_or_404(User, current_user.id)
            user.name = new_name
            db.session.commit()
            redirect(url_for("profile"))

    return render_template('pages/profile.html', name=current_user.name, score=current_user.highscore)

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/login', methods=['POST'])
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
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('pages/signup.html')

@app.route('/signup', methods=['POST'])
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
        return redirect(url_for('signup'))
    
    if not valid_password(password):
        flash('Weak Password')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Successful Signup! Please Login')
    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/test')
def test():
    stmt = db.select(Question)
    results = db.session.execute(stmt).scalars()
    data = results.all()
    for q in data:
        q.init_answers()

    return render_template('index.html', questions=data)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8888)