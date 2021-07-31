from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from models import db



class AdminLogin(UserMixin, db.Model):
    __tablename__ = "admin_login"
    id = Column(Integer, primary_key=True)
    username = Column(String(33), nullable=False, unique=True)
    password = Column(String(255), nullable=False, unique=True)
    remember = Column(Boolean, default=False)
