import flask

from is_safe_url import is_safe_url
from sqlalchemy import bindparam, select

from gendb import engine, ins, users
from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pwd1'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, email, pwd):
        self.id = id
        self.email = email
        self.pwd = pwd

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Users WHERE id = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id,user.email,user.pwd)

def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Users WHERE email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template("base.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT pwd FROM Users WHERE email = ?', [request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()
        if (real_pwd is not None ):
            if (request.form['pass'] == real_pwd['pwd']):
                user = get_user_by_email(request.form['user'])
                login_user(user)
                print(user)
                flask.flash('Logged in successfully.')
                if not is_safe_url("/private",{"http://127.0.0.1:5000/private"}):    #controllo sicurezza URL passato
                    return flask.abort(400)
                return redirect(url_for("private" or url_for('/')))
            else:
                return redirect(url_for('home')) # TODO implementare la logica di accesso a DBMS
        else :
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    conn = engine.connect()
    logout_user()
    conn.close()
    return redirect(url_for('home'))

@app.route('/private')
@login_required
def private():
    conn = engine.connect()
    users = current_user.get_id()
    resp = make_response(render_template("private.html", users=users))
    conn.close()
    return resp

@app.route('/sign_up')
def sign_up():
    return render_template("sign.html")


@app.route('/signing_up', methods=['GET', 'POST'])
def signing_up():   #TODO prima versione da sviluppare
    conn = engine.connect()
    user = request.form['user']
    pwd = request.form['pass']
    rs = conn.execute(select([users]).where(users.c.email == user))
    user_reg = rs.fetchone()
    if (user_reg is not None):
        return redirect(url_for('home'))
    conn.execute(ins, email=user, pwd=pwd)
    conn.close()
    return redirect(url_for('home'))


@app.route('/users/<username>')
def show_profile(username):
    users = ['alice','bob','charlie']
    if username in users:
        return render_template('profile.html', user=username)
    else:
        return render_template('profile.html', reg=users)

