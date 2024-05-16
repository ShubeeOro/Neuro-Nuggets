import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api.models import db, User, Question
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/leaderboard')
def leaderboard():
    users = db.session.query(User).order_by(desc(User.highscore))
    scores = []
    for i in users:
        temp = {}
        temp['name'] = i.name
        temp['highscore'] = i.highscore
        scores.append(temp)

    return render_template('pages/leaderboard.html', user=current_user, scores=scores)

# Shows profile
@main.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    if request.method == "POST":
        new_name = request.form["username"]
        if new_name:
            user = db.get_or_404(User, current_user.id)
            user.name = new_name
            db.session.commit()
            return redirect(url_for("main.profile"))

    return render_template('pages/profile.html', name=current_user.name, score=current_user.highscore)

