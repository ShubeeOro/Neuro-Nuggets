import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api.models import db, User
from flask_login import login_required, current_user
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash

play = Blueprint('play', __name__)

@play.route('/')
@login_required
def start_game():
    return render_template('pages/game_mode.html')

@play.route('/endless')
@login_required
def endless_game():
    return render_template('pages/endless.html')

@play.route('/solo')
@login_required
def solo_game():
    return render_template('pages/solo.html')

@play.route('/solo', methods=['POST'])
@login_required
def submit_score():
    score = request.form.get('new_score')
    user = db.get_or_404(User, current_user.id)
    print(score)
    print(user.highscore)
    if int(score) > int(user.highscore):
        user.highscore = int(score)
        db.session.commit()

    return redirect(url_for("main.leaderboard"))
