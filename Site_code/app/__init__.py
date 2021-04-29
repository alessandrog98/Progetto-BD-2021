from importlib import import_module

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from Site_code.gendb import generaDB


login_manager = LoginManager()

def register_extensions(app):
    #db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        tst=0

    @app.teardown_request
    def shutdown_session(exception=None):
        ts=0

def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    generaDB(app)

    return app


