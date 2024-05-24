import json
from api.models import Question, db
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 60,
    'pool_pre_ping': True
}

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = SQLALCHEMY_ENGINE_OPTIONS
    
# Initialize Database
db.init_app(app)

def import_data():
    with app.app_context():
        with open('trivia.json', 'r') as fp:
            data = json.load(fp)
            for row in data:
                obj = Question(
                        question=row['question'],
                        correct_answer=json.dumps(row['correct_answer']),
                        incorrect_answers=json.dumps(row['incorrect_answers']),
                        category=row['category'],
                        difficulty=row['difficulty']
                    )
                db.session.add(obj)
            db.session.commit()

if __name__ == "__main__":
    import_data()