from sqlalchemy import Column, Integer, String, LargeBinary
from opponent_app.models import db


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    data = Column(LargeBinary)
