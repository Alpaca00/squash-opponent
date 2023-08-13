from sqlalchemy import Column, Integer, String, Text

from opponent_app.models import db

# from sqlalchemy.orm import validates
# from marshmallow import fields, validate


class SupportMessage(db.Model):
    """SupportMessage model for storing messages."""
    __tablename__ = "messages"  # noqa
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    text = Column(Text, nullable=False)
