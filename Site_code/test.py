from gendb import engine,select_users
from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, UserMixin, current_user, login_required

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
    rs = conn . execute(select_users.where(current_user.get_id == '?'), user_id )
    user = rs.fetchone()
    conn.close()
    return User(user.id,user .email,user.pwd)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template("base.html")

@app.route ('/login', methods =['GET', 'POST'])
def login ():
    if request.method == 'POST':
        conn = engine . connect ()
        rs = conn.execute('SELECT pwd FROM Users WHERE email = ?', [ request.form ['user']])
        real_pwd = rs.fetchone ()
        conn.close ()
        if (real_pwd is not None ):
            return redirect(url_for('private')) # TODO implementare la logica di accesso a DBMS
        else :
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    if request.form['pass'] == real_pwd['pwd']:
        user = get_user_by_email(request.form['user'])
        login_user(user)
        return redirect(url_for('private'))
    else:
        return redirect(url_for('home'))

@app.route('/private')
@login_required
def private():
    conn = engine.connect()
    users = select_users
    resp = make_response(render_template(" private.html ", users=users))
    conn.close()
    return resp

@app.route('/users')
def users():
    return 'if u are a registerd user, please insert the username here: '

@app.route('/users/<username>')
def show_profile(username):
    users = ['alice','bob','charlie']
    if username in users:
        return render_template('profile.html', user=username)
    else:
        return render_template('profile.html', reg=users)

