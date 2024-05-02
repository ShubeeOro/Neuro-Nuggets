import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

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
    highscore = mapped_column(Integer(), nullable=True)

class Question(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    question = mapped_column(String(200), nullable=False, unique=True)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers = mapped_column(TEXT(400), nullable=False)
    category = mapped_column(String(100), nullable=False)
    difficulty = mapped_column(String(100), nullable=True)

    # Required to initalize the question from the database
    def init_answers(self) -> None:
        # Answer List
        answers = json.loads(self.incorrect_answers)
        answers.append(self.correct_answer)
        shuffle(answers)
        self.answers = answers
        self.answer_id  = answers.index(self.correct_answer) + 1

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