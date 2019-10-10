from flask import Flask, render_template, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from graph import build_graph
from config import CONNECT_STRING

import matplotlib.pyplot as plt
from io import BytesIO, StringIO

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
    masters = Master.query.all()

    for master in masters:
        slaves = Slave.query.filter_by(master_id=master.id).all()

        for slave in slaves:
            graph_url_list = []
            text = ''
            route = 'slaves/'
            slave_RXAddr = slave.RXAddr
            csv = '.txt'

            route += slave_RXAddr
            route += csv

            f = open(route, "r")
            texts = f.readlines()
            f.close()

            res_text = []
            text_list = []
            # for text in texts:
            #     text = text.replace('\n', '')
            #     res_text.append(text)

            for text in texts:
                text = text.replace('\n', '')
                text_list.append(text.split('|'))

            # x = KW, y = 시간
            x = []
            y = []

            for text in text_list[1:]:
                x.append(int(text[4]))
                y.append(int(text[1]) * 3600 + int(text[2]) * 60 + int(text[3]))

            print(x)
            print(y)

            graph_url = build_graph(y, x)
            graph_url_list.append(graph_url)

            slave.graph_url = graph_url

    return render_template('index.html', masters=masters, slaves=slaves)
    # return render_template('index.html')

# @app.route('/')
# def index():
#     return render_template('index.html')