from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from opponent_app.models import db


class Product(db.Model):
    """Product model for storing products."""
    __tablename__ = "products"  # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(String)
    is_new = Column(Boolean, nullable=False, default=False)
    add = Column(Boolean, nullable=False, default=False, server_default="false")
    deleted = Column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    t_shirts = db.relationship("TShirt", backref="products", lazy=True)


class TShirt(db.Model):
    """TShirt model for storing t-shirts."""
    __tablename__ = "t_shirts"  # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = db.relationship("Product", overlaps="products, t_shirts")


class Order(db.Model):
    """Order model for storing orders."""
    __tablename__ = "orders"  # noqa
    id = Column(Integer, primary_key=True)
    name_product = Column(String, nullable=False)
    print = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_total = Column(Float, nullable=False)
    users = db.relationship("User", backref="orders", lazy=True)
