import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
from array import array
from api.models import User, Question
from pathlib import Path
from flask import Flask
from sqlalchemy.sql import func
from random import randint
from db import db
from dotenv import load_dotenv

load_dotenv()
def init_temp_db():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'space-capybara'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URL")
    db.init_app(app)
    return app

app = init_temp_db()

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

    create_tables()
    import_question_data()

if __name__ == "__main__":
    import_question_data()
