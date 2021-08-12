from sqlalchemy import Column, Integer, String
from opponent_app.models import db


class VideoGallery(db.Model):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
