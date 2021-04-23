
from sys import exit
from decouple import config

from config import config_dict
from app import create_app

# WARNING: Don't run with debug turned on in production!
DEV = config('Dev', default=True)

# The configuration
get_config_mode = 'Dev' if DEV else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')





app = create_app(app_config)
app.run()
