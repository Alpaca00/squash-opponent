import re
from loguru import logger
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_validator import (
    Validator,
    ValidateInteger,
    ValidateString,
    ValidateEmail,
)
from opponent_app.models import db


class ValidatePhone(Validator):
    REGEX = r"^(?:\+38)?(?:\([0-9]{3}\D)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[0-9]{7}$gm"

    def check_value(self, value):
        if re.findall(self.REGEX, value):
            logger.info(value)
            return True
        else:
            raise AssertionError("Invalid phone number.")


class ValidatePassword(Validator):
    def check_value(self, value):
        if (
            not re.findall("\d", value)
            and not re.findall("[A-Z]", value)
            and not len(value) >= 8
        ):
            raise AssertionError(
                """The password must contain at least 1 digit, 0-9 and 1 uppercase letter,
                 A-Z and characters long must have more than 7."""
            )
        else:
            return True


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(33), nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String(255), nullable=False)
    address2 = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    zip_code = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = db.relationship("Order", overlaps="orders,users")

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


roles_users = db.Table('roles_users',
                       Column('user_account_id', Integer, ForeignKey('users_accounts.id')),
                       Column('role_id', Integer, ForeignKey('role.id')),
                       )


class UserAccount(db.Model, UserMixin):
    __tablename__ = "users_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(33), nullable=False, unique=True)
    password = Column(String, nullable=False)
    active = Column(Boolean)
    remember = Column(Boolean, default=False)
    users_opponent = db.relationship("UserOpponent", backref="users_account", lazy=True)
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref('users_accounts', lazy='dynamic')
    )

    @classmethod
    def __declare_last__(cls):
        ValidateString(UserAccount.name)
        ValidateEmail(UserAccount.email)
        ValidatePassword(UserAccount.password)


class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    description = Column(String(255))


user_datastore = SQLAlchemyUserDatastore(db, UserAccount, Role)


class UserOpponent(db.Model):
    __tablename__ = "users_opponents"
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=True, default="Amateur")
    city = Column(String(50))
    district = Column(String(50))
    date = Column(String(50))
    phone = Column(String(50))
    user_account_id = Column(Integer, ForeignKey("users_accounts.id"))
    user_account = db.relationship("UserAccount", overlaps="users_account,users_opponent")



class OfferOpponent(db.Model):
    __tablename__ = "offers_opponents"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    category = Column(String(50), nullable=True, default="Amateur")
    city = Column(String(50), default='Lviv')
    district = Column(String(50))
    date = Column(String(50))
    user_opponent_id = Column(Integer)
