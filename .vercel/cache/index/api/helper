from api.models import Question
from sqlalchemy.sql import func
from api.db import db

def load_random_question(app: Flask):
    with app.app_context():
        stmt = db.select(Question).order_by(func.random()).limit(1)
        result = db.session.execute(stmt).scalar()

    result.init_answers()
    return result