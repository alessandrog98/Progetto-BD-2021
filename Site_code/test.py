import flask

from is_safe_url import is_safe_url
from sqlalchemy import bindparam, select

from context import app, login_manager, engine, Session
from models import users
from models.users import User
from flask import render_template, redirect, url_for, request, make_response
from flask_login import current_user, login_required, login_user, logout_user

@app.route('/log')
def log():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template("accounts/login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.get_by_email(request.form['user'])
        if user is not None and user.check_password(request.form['pass']):
            login_user(user)
            flask.flash('Logged in successfully.')
            return redirect(url_for("private" or url_for('/')))
        else:
            return redirect(url_for('home'))


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_required
@app.route('/private')
def private():
    users = current_user.get_id()
    resp = make_response(render_template("private.html", users=users))
    return resp


@app.route('/sign_up')
def sign_up():
    return render_template("accounts/register.html")


@app.route('/signing_up', methods=['GET', 'POST'])
def signing_up():
     email = request.form['user']
     pwd = request.form['pass']
     s = Session()
     user_reg = User.get_by_email(email)
     if (user_reg is not None):
         return redirect(url_for('home'))
     new_user = User(email = email, name = email)
     new_user.set_password(pwd)
     s.add(new_user)
     s.commit()
     return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template("index.html")
