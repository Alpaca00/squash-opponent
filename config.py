# import os
#
# PG_HOST = os.environ['PG_HOST']

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@0.0.0.0:5432/alpaca"

SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/login"
SECURITY_POST_LOGOUT_VIEW = "/admin/logout"
