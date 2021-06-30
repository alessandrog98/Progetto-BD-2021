from flask import Flask
import context
from sys import exit
from decouple import config
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config_dict


# def register_extensions(app):
#     from context import login_manager
#     login_manager.init_app(app)


def register_blueprints(app):
    from modules.front import front
    from modules.login import auth
    from modules.survey import survey
    from modules.answer import answer
    app.register_blueprint(front, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/account')
    app.register_blueprint(survey, url_prefix='/survey')
    app.register_blueprint(answer, url_prefix='/answer')

def create_app():
    DEV = config('Dev', default=True)

    # The configuration
    get_config_mode = 'Dev' if DEV else 'Production'

    app_config = None
    try:
        # Load the configuration using the default values
        app_config = config_dict[get_config_mode.capitalize()]
    except KeyError:
        exit('Error: Invalid <config_mode>. Expected values [Dev, Production] ')

    context.app = Flask(__name__, instance_relative_config=True)
    context.app.config.from_object(app_config)

    context.engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
    context.Session = sessionmaker(bind=context.engine)

    context.login_manager = LoginManager(context.app)
    context.login_manager.init_app(context.app)

    import models
    import context_processor
    register_blueprints(context.app)

    context.SQLBase.metadata.bind = context.engine
    context.SQLBase.metadata.create_all(context.engine)

    return context.app