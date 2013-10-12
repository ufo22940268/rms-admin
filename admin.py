# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, DateField
from wtforms.validators import Required
import pymongo
from bson.objectid import ObjectId
from flask import Flask
from flask.ext import admin
from wtforms import form, fields
from flask.ext.admin.form import Select2Widget
from flask.ext.admin.contrib.pymongo import ModelView, filters
from flask.ext.admin.model.fields import InlineFormField, InlineFieldList
from util import *
from flask.ext.babelex import Babel
from datetime import date, timedelta, datetime

class ExampleForm(Form):
    field1 = TextField(u'用户名', id='username')
    field2 = TextField(u'密码', id='password')
    submit_button = SubmitField(u'提交')

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
    # highly recommend =)
    # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
                                         '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    return app

app = create_app()
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
# Initialize babel
babel = Babel(app)


# Create models
conn = pymongo.Connection()
db = conn.rms

class UserForm(form.Form):
    name = fields.TextField(u'用户名')
    password = fields.TextField(u'密码')
    valid_from = fields.DateTimeField(u'有效开始时间', default=datetime.today())
    valid_to = fields.DateTimeField(u'有效结束时间', default=date.today() + timedelta(days=365))

class SuperUserView(ModelView):
    column_list = ('name', 'password', 'valid_from', 'valid_to')
    column_sortable_list = ('name', 'password', 'valid_from', 'valid_to')

    form = UserForm

@app.route('/', methods=['POST', 'GET'])
def index():
    form = ExampleForm()
    if request.method == 'POST':
        if request.form['field1'] == "admin" and request.form['field2'] == 'admin':
            if is_mac():
                return redirect('http://127.0.0.1:5001/admin/super_userview/')
            else:
                return redirect('http://192.241.196.189:5001/admin/super_userview/')
        else:
            return render_template('failed.html', form=form)
    else:
        return render_template('index.html', form=form)

@babel.localeselector
def get_locale():
    return 'zh'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, u'用户管理系统')
    admin.locale_selector(get_locale)

    # Add views
    admin.add_view(SuperUserView(db.super_user, u'创建操作员'))
    if is_mac():
        host = '127.0.0.1'
    else:
        host = '192.241.196.189'

    if is_mac():
        debug = True
    else:
        debug = False
    app.run(host=host, port=5001, debug=debug)
