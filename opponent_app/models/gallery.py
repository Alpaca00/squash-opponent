from sqlalchemy import Column, Integer, LargeBinary, String

from opponent_app.models import db


class Gallery(db.Model):
    """Gallery model for storing images."""
    __tablename__ = "gallery"  # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    data = Column(LargeBinary)
