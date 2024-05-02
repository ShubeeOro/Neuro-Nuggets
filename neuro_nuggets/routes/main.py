import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from neuro_nuggets.models import Question, User
from flask_login import login_required, current_user
from neuro_nuggets.db import db
from flask import Blueprint, render_template, redirect, url_for, request, flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html', name=current_user.name)

@main.route('/test')
def test():
    stmt = db.select(Question)
    results = db.session.execute(stmt).scalars()
    data = results.all()
    for q in data:
        q.init_answers()

    return render_template('index.html', questions=data)