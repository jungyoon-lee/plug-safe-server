from flask import render_template, request, url_for, flash, jsonify, redirect
from flask_login import current_user

from app.forms.device import SdsForm, PlugForm
from app.models.device import Sds, Plug
from app import app, db


# Master 전용 ###############################################################

# Master에서 버튼 누르면 서버의 DB에 등록 시키는 통신
@app.route('sds/enroll', methods=('GET', 'POST'))
def enroll_sds():
    if request.method == 'POST':
        ipAddr = request.data['ipAddr']
        code = request.data['code']

        sdss = Sds(ipAddr=ipAddr, code=code)
        db.session.add(sdss)
        db.session.commit()

        return 'enroll success'
    return 'idontknow'


# Master에서 SDS의 DB에 변동 사항이 생겼는지 확인하는 통신
@app.route('sds/check', methods=('GET', 'POST'))
def check_sds():
    sdss = Sds.query.filter_by()

    if request.method == 'GET':

        if 'sds의 변경 사항있다':
            return 'plug'
        else:
            return '변경 사항 없음'

    return 'idontknow'


# Web 전용 ##################################################################

@app.route('/sds/create', methods=('GET', 'POST'))
def manage_sds():
    print(str(current_user.id))

    return ''


@app.route('/sds/<string:master_name>/<string:slave_name>/power_on')
def sds():
    return 0


@app.route('/plug', methods=('GET', 'POST'))
def plug():
    form = PlugForm(request.form)

    if request.method == 'POST' and form.validate():
        return 0

    return render_template('device/plug.html', form=form)