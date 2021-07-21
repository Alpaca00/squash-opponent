from sqlalchemy import Column, Integer, String
from models import db


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String(33), nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    address2 = Column(String, nullable=False, server_default='null')
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)


    # @email.setter
    def email(self, value):
        if len(value) > self.email.type.length:
            raise Exception("Value too long")
        self.email = value
        arr = [x for x in self.email]
        if '@' not in arr:
            raise Exception("The symbol @ must be in the field")