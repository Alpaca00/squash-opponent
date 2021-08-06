import os

# PG_HOST = os.environ['PG_HOST']
# SECRET_KEY_CA = os.environ['SECRET_KEY']


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@0.0.0.0:5432/alpaca"
    SECURITY_LOGIN_URL = "/login"
    SECURITY_LOGOUT_URL = "/account/logout"
    SECURITY_REGISTER_URL = "/register"
    SECURITY_POST_LOGIN_VIEW = "/admin/login"
    SECURITY_POST_LOGOUT_VIEW = "/admin/logout"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ['SPS']
    SECRET_KEY = '6Lf0rL8bAAAAAL0YqesYius-y0iQnYThoR-RWd0s'


class DevConfig(BaseConfig):
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = 'public'
    RECAPTCHA_PRIVATE_KEY = 'private'
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class ProdConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    TESTING = True


configurations = {
    'production': ProdConfig,
    'development': DevConfig,
    'test': TestConfig
}

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
