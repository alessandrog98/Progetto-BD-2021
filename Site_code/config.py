import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", ")J@NcRfUjXn2r5u8")

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

config_dict = {
    'Dev': DevelopmentConfig,
    'Production': ProductionConfig
}
