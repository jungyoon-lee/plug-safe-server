from app import db
from datetime import datetime

class Sds_code(db.Model):
    __tablename__ = "sds_codes"

    id = db.Column(db.Integer, primary_key=True)
    ipAddr = db.Column(db.String(15), primary_key=True)
    code = db.Column(db.Integer, primary_key=True)


class temp_master(db.Model):
    __tablename__ = "temp_masters"

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(20), primary_key=True)
    ipAddr = db.Column(db.String(20))
    auth = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.now)


class Master(db.Model):
    __tablename__ = "masters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    serial = db.Column(db.String(20), primary_key=True)
    ipAddr = db.Column(db.String(20))
    newdata = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.now)

    slaves = db.relationship('Slave', backref="master", lazy='dynamic')


class Slave(db.Model):
    __tablename__ = "slaves"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    RXAddr = db.Column(db.String(20))
    newdata = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    master_id = db.Column(db.Integer, db.ForeignKey('masters.id'))
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_date = db.Column(db.DateTime, default=datetime.now)