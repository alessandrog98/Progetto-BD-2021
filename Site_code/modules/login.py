import flask
import datetime

from flask_login import current_user, login_user, login_required, logout_user
from is_safe_url import is_safe_url
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from sqlalchemy.orm import session

from context import Session
from models.users import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("auth/login.html")
    else:
        user = User.get_by_email(request.form['user'])
        if user is not None and user.check_password(request.form['pass']):
            login_user(user, remember=True, duration=datetime.timedelta(minutes=20))
            flask.flash('Logged in successfully.')
            return redirect(url_for("auth.private"))
        else:
            return redirect(url_for('auth.login'))


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

        return render_template("auth/password_change_form.html")


@auth.route('/private')
@login_required
def private():
    users = current_user.get_id()
    resp = make_response(render_template("private.html", users=users))
    return resp


@auth.route('/sign_up')
def sign_up():
    return render_template("accounts/register.html")


@auth.route('/signing_up', methods=['GET', 'POST'])
def signing_up():   # TODO prima versione da sviluppare
    pass
    # conn = engine.connect()
    # user = request.form['user']
    # pwd_hash = generate_password_hash(request.form['pass'])
    # rs = conn.execute(select(User.c.email).where(User.c.email == user))
    # user_reg = rs.fetchone()
    # if (user_reg is not None):
    #     return redirect(url_for('auth.home'))
    # conn.execute(User.insert(), email=user, pwd=pwd_hash, IDGruppo=5)
    # conn.close()
    # return redirect(url_for('auth.home'))


@auth.route('/')
def home():
    return render_template("home.html")

