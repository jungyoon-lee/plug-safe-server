import json

from flask import render_template, request, url_for, flash, jsonify, redirect
from flask_login import current_user

from app.forms.device import SdsForm, PlugForm
from app.models.device import Master, Slave, temp_master
from app import app, db

def bytes_to_dict(bytes):
    string = bytes.decode('ASCII')
    dict = json.loads(string)

    return dict

############################## Master 전용 ##############################

# Master에서 버튼 누르면 서버의 DB에 등록 시키는 통신
@app.route('/master/serial', methods=['GET', 'POST'])
def serial():
    if request.method == 'POST':
        data_bytes = request.data
        data_dict = bytes_to_dict(data_bytes)

        serial = data_dict["serial"]
        ipAddr = data_dict["ipAddr"]

        masters = temp_master.query.filter_by(serial=serial).all()

        error = None

        if masters:
            error = '이미 마스터 시리얼 번호가 등록됨'

        if error is None:
            new_master = temp_master(ipAddr=ipAddr, serial=serial)
            db.session.add(new_master)
            db.session.commit()

        flash(error)

    return 'i dont know'


#
@app.route('/master/<string:serial>/slaves', methods=['GET', 'POST'])
def master_slaves(serial):
    if request.method == 'GET':
        master = Master.query.filter_by(serial=serial).one()
        slaves = Slave.query.filter_by(master_id=master.id).all()

        connected = len(slaves)
        RXAddr = []

        for slave in slaves:
            RXAddr.append(slave.RXAddr)

        data = {}

        data["connected"] = connected
        data["RXAddr"] = RXAddr

        return jsonify(data)


############################## Slave 전용 ##############################

#



############################## Web 전용 ################################

# 대쉬보드
@app.route('/master/dashboard', methods=['GET', 'POST'])
def master_dashboard():
    masters = Master.query.filter_by(user_id=current_user.id).all()

    if masters is not None:
        return render_template('device/master_dashboard.html', masters=masters)

    return render_template('device/master_dashboard.html', masters=None)


@app.route('/master/<string:master_id>/control')
def master_control(master_id):
    master = Master.query.filter_by(id=master_id).first()
    slaves = Slave.query.filter_by(master_id=master.id).all()

    return render_template('device/master_control.html', master=master, slaves=slaves)


@app.route('/master/<string:master_id>/slave/<string:slave_id>/control', methods=['POST'])
def slave_control(master_id, slave_id):
    switch = request.form['switch']

    slave = Slave.query.filter_by(id=slave_id).first()

    if switch is 'on':
        slave.state = 'off'
    else:
        slave.state = 'on'

    db.session.commit()

    return redirect(url_for('master_control', master_id=master_id))


@app.route('/master/<string:master_id>/slave/all/off', methods=['POST'])
def slave_all(master_id):
    slaves = Slave.query.filter_by(master_id=master_id).all()

    for slave in slaves:
        slave.state = 'off'
        db.session.commit()

    return redirect(url_for('master_control', master_id=master_id))


# 시리얼 확인 하는 구간
@app.route('/master/enroll/check', methods=['GET', 'POST'])
def master_enroll_check():
    if request.method == 'POST':
        serial = request.form['serial']

        error = None

        master = temp_master.query.filter_by(serial=serial).first()

        if master is None:
            error = '사용 할 수 없는 시리얼 입니다.'

        elif master.auth is True:
            error = '이미 사용된 시리얼 번호입니다.'

        if error is None:
            return redirect(url_for('master_enroll', serial=master.serial))

        flash(error)

    return render_template('device/master_enroll_check.html')


# 시리얼 확인 후 웹에서 마스터 등록 (master: name, serial)
@app.route('/master/enroll/<string:serial>', methods=['GET', 'POST'])
def master_enroll(serial):
    master = temp_master.query.filter_by(serial=serial).first()

    if request.method == 'POST':
        name = request.form['name']

        new_master = Master(name=name, serial=master.serial, ipAddr=master.ipAddr, user_id=current_user.id)
        db.session.add(new_master)
        db.session.commit()

        flash('성공')
        return render_template('device/master_enroll_complete.html')

    return render_template('device/master_enroll.html', serial=master.serial, ipAddr=master.ipAddr)


# Slave 웹 등록
@app.route('/master/<string:master_id>/slave/enroll', methods=['GET', 'POST'])
def slave_enroll(master_id):
    if request.method == 'POST':
        RXAddr = request.form['RXAddr']
        name = request.form['name']

        error = None

        slaves = Slave.query.filter_by(RXAddr=RXAddr).all()

        if slaves is None:
            error = '이미 사용된 주소입니다.'

        if error is None:
            slave = Slave(RXAddr=RXAddr, name=name, master_id=master_id, user_id=current_user.id)
            db.session.add(slave)
            db.session.commit()

            flash('성공')
            return render_template('device/slave_enroll_complete.html')

        flash(error)

    return render_template('device/slave_enroll.html', master_id=master_id)

#######################################################################