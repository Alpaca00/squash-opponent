from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models import db
# from sqlalchemy.orm import validates
# from marshmallow import fields, validate


class SupportMessage(db.Model):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    text = Column(Text, nullable=False)
