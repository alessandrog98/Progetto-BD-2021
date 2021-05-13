from decouple import config


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = config("SECRET_KEY", default=")J@NcRfUjXn2r5u8")
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE'),
        config('DB_USER'),
        config('DB_PASSWORD'),
        config('DB_ADDRESS'),
        config('DB_PORT'),
        config('DB_NAME')
    )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


config_dict = {
    'Dev': DevelopmentConfig,
    'Production': ProductionConfig
}
