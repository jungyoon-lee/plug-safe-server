from app import db
from datetime import datetime

class Sds(db.Model):
    __tablename__ = ""

    id = db.Column(db.Integer, primary_key=True)
    ipAddr = db.Column(db.String(15), primary_key=True)
    code = db.Column(db.Integer, primary_key=True)


class Sds(db.Model):
    __tablename__ = "sdss"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.now)

    plugs = db.relationship('Plug', backref="sds", lazy='dynamic')


class Plug(db.Model):
    __tablename__ = "plugs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sds_id = db.Column(db.Integer, db.ForeignKey('sdss.id'))
    newdata = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.now)