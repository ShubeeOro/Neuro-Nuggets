from flask import Flask, redirect, url_for, render_template, redirect, url_for, request
from pathlib import Path 
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO, send, emit
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
import json

load_dotenv()

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
app.config['SECRET_KEY'] = os.environ.get('POSTGRES_URL')


# Blueprints
#app.register_blueprint(auth, url_prefix="/")
#app.register_blueprint(main, url_prefix="/")
#app.register_blueprint(play, url_prefix="/play")

# Database Models
from sqlalchemy import ForeignKey, Integer, String, TEXT
from flask_login import UserMixin
from sqlalchemy.orm import mapped_column, relationship
from random import shuffle 
from neuro_nuggets.db import db
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


# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# App
app.route('/')
def index():
    return "Hi"

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
            redirect(url_for("main.profile"))

    return render_template('pages/profile.html', name=current_user.name, score=current_user.highscore)

@app.route('/test')
def test():
    stmt = db.select(Question)
    results = db.session.execute(stmt).scalars()
    data = results.all()
    for q in data:
        q.init_answers()

    return render_template('index.html', questions=data)