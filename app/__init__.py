from flask import Flask, render_template, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import numpy as np

from graph import build_graph
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
    f = open("slaves/Sds01", "r")
    texts = f.readlines()
    f.close()

    res_text = []

    for text in texts:
        text = text.replace('\n', '')
        res_text.append(text)

    temp_text = res_text[10:]

    x = [0, 10, 20, 30, 40, 50, 60]
    y = []

    for i in temp_text:
        y.append(int(i[9:]))

    x1 = [0, 1, 2, 3, 4]
    y1 = [10, 30, 40, 5, 50]
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]

    graph1_url = build_graph(x1, y1);
    graph2_url = build_graph(x2, y2);
    graph3_url = build_graph(x3, y3);

    graph = build_graph(x1, y1)

    return render_template('index.html', graph=graph1_url)
    # return render_template('index.html')