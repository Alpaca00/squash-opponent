from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float
from models import db


# class Product(db.Model):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     name_product = Column(String, nullable=False)
#     is_new = Column(Boolean, nullable=False, default=False)
#     add = Column(Boolean, nullable=False, default=False, server_default='false')
#     deleted = Column(Boolean, nullable=False, default=False, server_default='false')
#     characters = db.relationship("Character", backref="products", lazy=True)
#
#
# class Character(db.Model):
#     __tablename__ = "character"
#     id = Column(Integer,  primary_key=True)
#     size = Column(String, nullable=False)
#     sex = Column(String, nullable=False)
#     character_description = Column(Text(), nullable=False)
#     product_id = Column(Integer, ForeignKey('products.id'))
#     product = db.relationship('Product')


class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(String)
    is_new = Column(Boolean, nullable=False, default=False)
    add = Column(Boolean, nullable=False, default=False, server_default='false')
    deleted = Column(Boolean, nullable=False, default=False, server_default='false')
    t_shirts = db.relationship("TShirt", backref="products", lazy=True)
    # orders = db.relationship("Orders", backref="products", lazy=True)


class TShirt(db.Model):
    __tablename__ = "t_shirts"
    id = Column(Integer,  primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = db.relationship('Product')


# class Order(db.Model):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True)
#     name_product = Column(String, nullable=False)
#     print = Column(String, nullable=False)
#     order_total = Column(Float, nullable=False)
#     product_id = Column(Integer, ForeignKey('products.id'))
#     product = db.relationship('Product')
#     users = db.relationship("Users", backref="orders", lazy=True)
