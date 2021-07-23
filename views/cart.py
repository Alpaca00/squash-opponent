from typing import Any, Optional
from flask import Blueprint, render_template, request
from werkzeug.exceptions import BadRequest, RequestTimeout
from ast import literal_eval
from models import Product, db, User
from views.product import cache


cart_app = Blueprint("cart_app", __name__)
id: Any = None


@cart_app.route("/<int:cart_id>/", methods=['GET', 'POST'])
def cart_list(cart_id: int):
    global id
    id = cart_id
    print(id)
    if cart_id is None:
        raise BadRequest(f"Invalid product id #{cart_id}")
    cart = Product.query.filter_by(id=cart_id).one_or_none()
    convert = cache.get('cart')
    if convert is not None:
        cart_items = literal_eval(convert.decode('ascii'))
    else:
        link = "http://192.168.1.18:5000/products/"
        raise RequestTimeout(f'Your order time has expired. Please follow the link: {link}')
    if request.method == 'GET':
        cart.add = True
        db.session.commit()
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        user = User(first_name=first_name, last_name=last_name,
                    email=email, phone=phone, address=address,
                    address2=address2, city=city, state=state,
                    zip_code=zip_code
                    )
        db.session.add(user)
        db.session.commit()
        order_user = User.query.filter_by(phone=phone).all()
        return render_template("order/index.html", orders_user=order_user, product=cart, cart_items=cart_items)
    return render_template("cart/index.html", product=cart, cart_items=cart_items)



@cart_app.route("/")
def empty_list(id_cart=None):
    id_cart = id
    if id_cart is None:
        return render_template("cart/empty.html")
    else:
        return cart_list(id_cart)
