import json
from array import array
from models import User, Question
from pathlib import Path
from flask import Flask
from sqlalchemy.sql import func
from random import randint
from neuro_nuggets.db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'space-capybara'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
app.instance_path = Path("data/storage.db").resolve()
db.init_app(app)

def import_question_data():
    with app.app_context():
        with open('data/trivia.json', 'r') as fp:
            data = json.load(fp)
            for row in data:
                obj = Question(
                    question=str(row['question']),
                    difficulty=str(row['difficulty']).lower(),
                    category=str(row['category']),
                    correct_answer=str(row['correct_answer']),
                    incorrect_answers=json.dumps(row['incorrect_answers']),
                    )
                db.session.add(obj)
            db.session.commit()

def create_tables():
    with app.app_context():
        db.create_all()

def drop_tables():
    with app.app_context():
        db.drop_all()

def reset():
    drop_tables()
    create_tables()
    import_question_data()

if __name__ == "__main__":
    reset()
