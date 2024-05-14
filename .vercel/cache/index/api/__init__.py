from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from api.index import create_app

class Base(DeclarativeBase):
    pass

app = create_app()

db = SQLAlchemy(app=app,model_class=Base)