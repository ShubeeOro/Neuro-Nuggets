from db import db
from models import User, Question
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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
            redirect(url_for("main.profile"))

    return render_template('pages/profile.html', name=current_user.name, score=current_user.highscore)

    


@main.route('/test')
def test():
    stmt = db.select(Question)
    results = db.session.execute(stmt).scalars()
    data = results.all()
    for q in data:
        q.init_answers()

    return render_template('index.html', questions=data)