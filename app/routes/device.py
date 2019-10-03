import json

from flask import render_template, request, url_for, flash, jsonify, redirect, abort
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from app.forms.device import SdsForm, PlugForm
from app.models.device import Master, Slave, temp_master
from app import app, db

from threading import Thread
from socket_server import runSocketServer, host

def bytes_to_dict(bytes):
    string = bytes.decode('ASCII')
    dict = json.loads(string)

    return dict

############################## Master 전용 ##############################

@app.route('/socket_start')
def socket_start():
    socket = Thread(target=runSocketServer, args=(db))
    socket.daemon = True
    socket.start()

    return render_template('index.html')


# DB 바뀐지 체크 후 바뀐다면 전송
@app.route('/master/change', methods=['GET', 'POST'])
def change():
    if request.method == 'POST':
        pass


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

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        flash(error)
        return '성공'

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

# 슬레이브 컨트롤
@app.route('/master/<int:master_id>/slave/<int:slave_id>/control/<string:switch>', methods=['POST'])
def slave_control(master_id, slave_id, switch):
    master = Master.query.filter_by(id=master_id).first()
    slave = Slave.query.filter_by(id=slave_id).first()

    if switch == 'on':
        slave.state = slave.newdata = master.newdata = 1
    else:
        slave.state = 0
        slave.newdata = master.newdata = 1

    db.session.add(slave)
    db.session.add(master)
    db.session.commit()

    return redirect(url_for('master_control', master_id=master_id))

# 마스터에 딸려 있는 슬레이브들 다 끄기
@app.route('/master/<int:master_id>/slave/all/off', methods=['POST'])
def slave_all(master_id):
    slaves = Slave.query.filter_by(master_id=master_id).all()

    for slave in slaves:
        slave.state = 0
        db.session.add(slave)
        db.session.commit()

    return redirect(url_for('master_control', master_id=master_id))


############################## Web 전용 ################################

# 대쉬보드
@app.route('/master/dashboard', methods=['GET', 'POST'])
def master_dashboard():
    masters = Master.query.filter_by(user_id=current_user.id).all()

    if masters is not None:
        return render_template('device/master_dashboard.html', masters=masters)
        
    return render_template('device/master_dashboard.html', masters=None)


@app.route('/master/<int:master_id>/control')
def master_control(master_id):
    master = Master.query.filter_by(id=master_id).first()
    slaves = Slave.query.filter_by(master_id=master.id).all()

    return render_template('device/master_control.html', master=master, slaves=slaves)


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
        master.auth = 1

        db.session.add(new_master)
        db.session.add(master)
        db.session.commit()

        flash('성공')
        return render_template('device/master_enroll_complete.html')

    return render_template('device/master_enroll.html', serial=master.serial, ipAddr=master.ipAddr)


# Slave 웹 등록
@app.route('/master/<int:master_id>/slave/enroll', methods=['GET', 'POST'])
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

# 무한 get
@app.route('/master/<string:master_serial>/change/check', methods=['GET', 'POST'])
def infinity_get(master_serial):
    master = Master.query.filter_by(serial=master_serial).first()
    slaves = Slave.query.filter_by(master_id=master.id, newdata=1).all()

    if request.method == 'POST':
        master.newdata = 0

        for slave in slaves:
            slave.newdata = 0
            db.session.add(slave)

        db.session.add(master)
        db.session.commit()

        return 'change'

    if master.newdata == 0:
        abort(500)

    newdata = 1
    slaves_addr = []
    changes = 0
    states = []

    for slave in slaves:
        slaves_addr.append(slave.RXAddr)
        changes += 1

        if slave.state == 1:
            states.append(1)
        else:
            states.append(0)


    data = {'newdata': newdata, 'changes': changes, 'slaves_addr': slaves_addr, 'states': states}

    return data