from sqlalchemy import Column, Integer, String
from models import db


# server
class VideoGallery(db.Model):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
