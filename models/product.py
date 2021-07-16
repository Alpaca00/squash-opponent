from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from models import db


class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    name_product = Column(String, nullable=False)
    is_new = Column(Boolean, nullable=False, default=False)
    add = Column(Boolean, nullable=False, default=False, server_default='false')
    deleted = Column(Boolean, nullable=False, default=False, server_default='false')
    characters = db.relationship("Character", backref="products", lazy=True)


class Character(db.Model):
    __tablename__ = "character"
    id = Column(Integer,  primary_key=True)
    size = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    character_description = Column(Text(), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = db.relationship('Product')

