from sys import exit
from decouple import config
from flask_login import LoginManager
from sqlalchemy import create_engine

from config import config_dict
from context import context
from app import create_app

if __name__ == "__main__":
    # WARNING: Don't run with debug turned on in production!
    DEV = config('Dev', default=True)

    # The configuration
    get_config_mode = 'Dev' if DEV else 'Production'

    try:
        # Load the configuration using the default values
        app_config = config_dict[get_config_mode.capitalize()]
    except KeyError:
        exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

    context.app = create_app(app_config)

    context.engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
    context.login_manager = LoginManager(context.app)

    context.login_manager.init_app(context.app)

    import models
    context.SQLBase.metadata.create_all(context.engine)

    context.app.run()
