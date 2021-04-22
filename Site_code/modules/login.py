import flask
import sqlalchemy
import datetime

from sqlalchemy import select, Column, Integer, String
from flask_login import LoginManager, UserMixin, AnonymousUserMixin, current_user, login_user, login_required, logout_user
from is_safe_url import is_safe_url
from flask import Flask, render_template, redirect, url_for, request, make_response,Blueprint
from gendb import users
from config import conn_str, engine
from models.users import User

auth = Blueprint('auth', __name__)

def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute(select(users).where(users.c.email == email))
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)

@auth.route('/log')
def log():
    if current_user.is_authenticated:
        return redirect(url_for('auth.private'))
    return render_template("log.html")

@auth.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(select(users.c.pwd).where(users.c.email == request.form['user']))
        password = rs.fetchone()
        conn.close()
        if (password is not None ):
            if (request.form['pass'] == password['pwd']):
                user = get_user_by_email(request.form['user'])
                login_user(user, remember=True, duration=datetime.timedelta(minutes=20))
                print(user)
                flask.flash('Logged in successfully.')
                if not is_safe_url("/private",{"http://127.0.0.1:5000/private"}):    #controllo sicurezza URL passato
                    return flask.abort(400)
                return redirect(url_for('auth.private'))
            else:
                return redirect(url_for('auth.home'))
        else:
            return redirect(url_for('auth.home'))
    else:
        return redirect(url_for('auth.home'))



@auth.route('/logout')
@login_required
def logout():
    conn = engine.connect()
    logout_user()
    conn.close()
    return redirect(url_for('auth.home'))

@auth.route('/private')
@login_required
def private():
    conn = engine.connect()
    users = current_user.get_id()
    resp = make_response(render_template("private.html", users=users))
    conn.close()
    return resp

@auth.route('/sign_up')
def sign_up():
    return render_template("sign.html")


@auth.route('/signing_up', methods=['GET', 'POST'])
def signing_up():   #TODO prima versione da sviluppare
    conn = engine.connect()
    user = request.form['user']
    pwd = request.form['pass']
    rs = conn.execute(select(users.c.email).where(users.c.email == user))
    user_reg = rs.fetchone()
    if (user_reg is not None):
        return redirect(url_for('auth.home'))
    conn.execute(users.insert(), email=user, pwd=pwd, IDGruppo=5)
    conn.close()
    return redirect(url_for('auth.home'))


@auth.route('/')
def home():
    return render_template("home.html")
