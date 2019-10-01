from flask import Flask, render_template, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import CONNECT_STRING

from socket import *
# from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT_STRING
app.config['SECRET_KEY'] = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from app import models
db.create_all()

from app import routes


@app.route('/')
def index():
    return render_template('index.html')