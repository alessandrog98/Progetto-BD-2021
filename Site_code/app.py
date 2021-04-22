from flask import Flask
from flask_login import LoginManager
from sqlalchemy import select
from models.users import User

from config import engine
from gendb import users
from utils.conn import Userquery

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'pwd1'

    login_manager = LoginManager()
    login_manager.init_app(app)


    #blueprint.auth

    @login_manager.user_loader
    def load_user(user_id):
        conn = engine.connect()
        rs = conn.execute(select(users).where(users.c.id == user_id))
        user = rs.fetchone()
        conn.close()
        return User(user.id, user.email, user.pwd)

    from modules.login import auth as auth
    app.register_blueprint(auth)

    return app
