from sqlalchemy import Column, Integer, String
from models import db
from flask_login import UserMixin


class AdminLogin(db.Model, UserMixin):
    __tablename__ = "admin_login"
    id = Column(Integer, primary_key=True)
    name = Column(String(33), nullable=False)
