import os

PG_HOST = os.environ.get("PG_HOST")


class BaseConfig:
    """Base configuration."""
    SECURITY_LOGIN_URL = "/login"
    SECURITY_LOGOUT_URL = "/account/logout"
    SECURITY_REGISTER_URL = "/register"
    SECURITY_POST_LOGIN_VIEW = "/admin/login"
    SECURITY_POST_LOGOUT_VIEW = "/admin/logout"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ["SPS"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    BABEL_DEFAULT_LOCALE = "en"
    LANGUAGES = ["en", "uk"]
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "public"
    RECAPTCHA_PRIVATE_KEY = "private"
    RECAPTCHA_OPTIONS = {"theme": "dark"}


class DevConfig(BaseConfig):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://user:password@0.0.0.0:5432/alpaca"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(BaseConfig):
    """Production configuration."""
    # SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://user:password@{PG_HOST}:5432/alpaca"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://user:password@127.0.0.1:5432/alpaca"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    """Test configuration."""
    TESTING = True


configurations = {
    "production": ProdConfig,
    "development": DevConfig,
    "test": TestConfig,
}

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.environ["EMAIL_USERNAME"],
    "MAIL_PASSWORD": os.environ["EMAIL_PASSWORD"],
}
