import json
from flask import render_template, request, url_for, flash, jsonify, redirect
from flask_login import current_user

from app.forms.device import SdsForm, PlugForm
from app.models.device import Master, Slave, temp_master
from app import app, db


# Master 전용 ###############################################################

# Master에서 버튼 누르면 서버의 DB에 등록 시키는 통신
@app.route('/master/serial', methods=['GET', 'POST'])
def serial():
    if request.method == 'POST':
        ipAddr = request.ip
        serial = request.ip

        masters = Master.query.filter_by(serial=serial).all()

        if masters:
            error = '이미 마스터 시리얼 번호가 등록됨'

        if error is None:
            new_master = temp_master(ipAddr=ipAddr, serial=serial)
            db.session.add(new_master)
            db.session.commit()

        flash(error)

    return 'i dont know'


# 웹에서 마스터 등록 (master: name, serial)
@app.route('/master/enroll', methods=['GET', 'POST'])
def enroll_master():
    if request.method == 'POST':
        name = request.data['name']
        serial = request.data['serial']

        master = temp_master.query.filter_by(serial=serial).first()

        if master is not None:
            new_master = Master(name=name, serial=serial)
            db.session.add(new_master)
            db.session.commit()

            flash('성공')
            return redirect(url_for('index'))

        flash('serial 번호가 없거나 사용 되었습니다.')
        return redirect(url_for('enroll'))

    return render_template('master/enroll.html')


#

# Web 전용 ##################################################################

# 스디스 생성, 수정
@app.route('/sds/create', methods=('GET', 'POST'))
def manage_sds():
    print(str(current_user.id))

    return ''


# 플러그 작동
@app.route('/sds/<string:master_name>/<string:slave_name>/power_on')
def sds():
    return 0


@app.route('/plug', methods=['GET', 'POST'])
def plug():
    form = PlugForm(request.form)

    if request.method == 'POST' and form.validate():
        return 0

    return render_template('device/plug.html', form=form)