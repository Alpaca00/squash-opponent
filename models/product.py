from sqlalchemy import Column, Integer, String, Boolean

from models import db


class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    name_product = Column(String, nullable=False)
    is_new = Column(Boolean, nullable=False, default=False)
    add = Column(Boolean, nullable=False, default=False, server_default='false')
    deleted = Column(Boolean, nullable=False, default=False, server_default='false')
