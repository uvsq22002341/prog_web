import os
from functools import wraps
from flask import Flask, render_template, request, redirect, session, url_for
from jinja2 import StrictUndefined
from flask_app import model
from flask_session import Session
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import BooleanField, StringField, PasswordField, EmailField, validators, DateField
import pyotp
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = True
app.jinja_env.undefined = StrictUndefined
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
CSRFProtect(app)
QRcode(app)

from flask_talisman import Talisman
Talisman(app, content_security_policy={
  'default-src' : '\'none\'',
  'style-src': [ 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css' ],
  'img-src' : ['\'self\'', 'data:'],
  'script-src' : '\'none\''
})

def login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not 'user' in session:
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return wrapper


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


class LoginForm(FlaskForm):
  email = EmailField('email', validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired()])
  totp = StringField('totp')

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      user = model.get_user(connection, form.email.data, form.password.data)
      totp = model.get_totp(connection, user['id'])
      if totp is not None and not pyotp.TOTP(totp).verify(form.totp.data):
          raise Exception('Double authentification invalide')
      session['user'] = user
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
  session.pop('user')
  return redirect('/')


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('oldPassword', [validators.DataRequired()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirmPassword', 
                           message='Les mots de passe doivent correspondre')
    ])
    confirmPassword = PasswordField('confirmPassword', [validators.DataRequired()])
    totpEnabled = BooleanField('totpEnabled')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  email = session['user']['email']
  form = ChangePasswordForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      totp_secret = session['totp_secret'] if form.totpEnabled.data else None
      model.change_password(connection, 
                            email, 
                            form.oldPassword.data,
                            form.password.data)
      model.change_totp(connection, email, totp_secret)
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  totp_secret = pyotp.random_base32()
  totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=email, issuer_name='SoccerApp')
  session['totp_secret'] = totp_secret
  return render_template('change_password.html', form=form, totp_uri=totp_uri)


class CreateUserForm(FlaskForm):
    email = EmailField('email', validators=[validators.DataRequired()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirmPassword', 
                           message='Les mots de passe doivent correspondre')
    ])
    confirmPassword = PasswordField('confirmPassword', [validators.DataRequired()])


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
  form = CreateUserForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      model.add_user(connection, form.email.data, form.password.data)
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('create_user.html', form=form)






