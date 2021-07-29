import re
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from flask_validator import Validator, ValidateInteger, ValidateString, ValidateEmail
from models import db
from app import logger


class ValidatePhone(Validator):
    REGEX = r'^(?:\+38)?(?:\([0-9]{3}\D)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[0-9]{7}$gm'

    def check_value(self, value):
        if re.findall(self.REGEX, value):
            logger.info(value)
            return True
        else:
            raise AssertionError("Invalid phone number.")



class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(33), unique=True)
    phone = Column(String, nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    address2 = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    zip_code = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = db.relationship("Order")


    @classmethod
    def __declare_last__(cls):
        ValidateString(User.full_name)
        ValidateEmail(User.email)
        ValidatePhone(User.phone)
        ValidateString(User.address)
        ValidateString(User.address2)
        ValidateString(User.city)
        ValidateString(User.state)
        ValidateInteger(User.zip_code)




class UserAccount(db.Model):
    __tablename__ = "users_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    logout = Column(Boolean, default=False, server_default="false")
    users_opponent = db.relationship("UserOpponent", backref="users_account", lazy=True)


class UserOpponent(db.Model):
    __tablename__ = "users_opponents"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=True, default="Amateur")
    city = Column(String, nullable=False)
    district = Column(String, nullable=True)
    user_account_id = Column(Integer, ForeignKey('users-accounts.id'))
    user_account = db.relationship('UserAccount')

