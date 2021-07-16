from flask import Blueprint, render_template, request
from models import Product, db

cart_app = Blueprint("cart_app", __name__)


@cart_app.route("/", methods=['GET', 'POST'])
def cart_list():
    cart = Product.query.filter_by(id=4).one_or_none()
    if request.method == 'GET':
        cart.add = True
        db.session.commit()
    return render_template("cart/index.html", product=cart)
