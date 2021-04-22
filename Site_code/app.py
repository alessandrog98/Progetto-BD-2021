from flask import Flask
from flask_login import LoginManager
from utils.conn import Userquery

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'pwd1'

    login_manager = LoginManager()
    login_manager.init_app(app)


    #blueprint .auth
    from models.users import User
    @login_manager.user_loader
    def load_user(user_id):
        user = Userquery(user_id)
        return user

    from modules.login import auth as auth
    app.register_blueprint(auth)

    return app
