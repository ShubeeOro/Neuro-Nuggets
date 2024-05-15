import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import re
from unittest.mock import patch

import pytest

from neuro_nuggets.models import Question

# This becomes a variable based on function name (question)
# You can pass this through other test func to have a preset variable
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

