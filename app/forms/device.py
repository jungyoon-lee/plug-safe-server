from wtforms import Form, StringField

class SdsForm(Form):
    name = StringField('스디스 이름')


class PlugForm(Form):
    name = StringField('플러그 이름')