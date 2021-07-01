import flask
import datetime

from flask_login import current_user, login_user, login_required, logout_user
from flask import render_template, redirect, url_for, request, make_response, Blueprint, flash
from werkzeug.urls import url_parse

from context import Session
from models.users import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("auth/login.html")
    else:
        next_page = request.form['next']
        user = User.get_by_email(request.form['user'])
        if user is not None and user.check_password(request.form['pass']):
            login_user(user, remember=True, duration=datetime.timedelta(minutes=20))
            default = url_for('front.home')
        else:
            flask.flash('Wrong username or password')
            default = url_for('auth.login')
        if not next_page or next_page == 'None' or url_parse(next_page).netloc != '':
            next_page = default
        return redirect(next_page)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("auth/logged_out.html")


@auth.route('/password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    if request.method == 'GET':
        return render_template("auth/password_change_form.html")
    else:
        s = Session()
        user: User = s.query(User).filter_by(id=current_user.id).first()
        old = request.form["old_password"]
        new1 = request.form["new_password1"]
        new2 = request.form["new_password2"]

        if user.check_password(old):  # TODO show errors
            if new1 == new2 and new1 != "":
                user.set_password(new1)
                s.commit()
                return render_template("auth/password_change_done.html")
            else:
                # TODO Show error password mismatch
                return render_template("auth/password_change_form.html")
        else:
            # TODO Show error wrong old password
            return render_template("auth/password_change_form.html")


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("auth/signup.html")
    else:
        email = request.form['user']
        pwd = request.form['pass']
        s = Session()
        if User.get_by_email(email) is None:
            new_user = User(email=email, name=email)
            new_user.set_password(pwd)
            s.add(new_user)
            s.commit()
            return redirect(url_for('front.home'))
        flash('email già esistente ! prova ad accedere')
        return redirect(url_for('auth.sign_in'))


@auth.route('/reservedarea')
@login_required
def reservedarea():
    data = User.my_surveys(current_user.get_id())
    return render_template("front/reserved.html", data=data)

