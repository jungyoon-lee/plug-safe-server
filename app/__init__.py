from flask import Flask, render_template, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import CONNECT_STRING

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_STRING
app.config['SECRET_KEY'] = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

engine = create_engine("mysql://root:111111@localhost:3306/sds")
session_factory = sessionmaker(autoflush=True, autocommit=False, bind=engine)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
session = scoped_session(session_factory)

from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from app import models
db.create_all()

from app import routes

from app.models.device import Master, Slave

@app.route('/')
def index():
    db_session = session()
    master = db_session.query(Master).filter(Master.id == 1).one()
    return render_template('index.html')