import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask, url_for, request, flash
import os
from dotenv import load_dotenv
from api.models import db, Question
import pytest

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')

# Initialize Database
db.init_app(app)

@pytest.fixture
def question():
    """Fixture with set question and answers"""
    q = Question(
        question="Question text",
        difficulty="medium",
        category="category",
        correct_answer="correct",
        incorrect_answers='["wrong", "false", "incorrect"]',
    )
    
    q.answers = ["correct", "wrong", "false", "incorrect"]
    q.answer_id = 1
    return q

def test_question(question):

    assert question.question == "Question text"
    assert "correct" in question.answers
    assert "incorrect" in question.answers
    assert question.difficulty == "medium"
    assert question.category == "category"

def test_question_convert(question):

    q = question.convert_question()
    
    assert q['question'] == "Question text"
    assert q['answer_id'] == 1
    assert q['answers'] == ["correct", "wrong", "false", "incorrect"]
    assert q['correct_answer'] == "correct"

