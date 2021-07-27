from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from models import db


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String(33), unique=True)
    phone = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    address2 = Column(String, nullable=False, server_default='null')
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = db.relationship('Order')




class UserAccount(db.Model):
    __tablename__ = "users_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    logout = Column(Boolean, default=False, server_default='false')

    # @email.setter
    # def email(self, value):
    #     if len(value) > self.email.type.length:
    #         raise Exception("Value too long")
    #     self.email = value
    #     arr = [x for x in self.email]
    #     if '@' not in arr:
    #         raise Exception("The symbol @ must be in the field")
