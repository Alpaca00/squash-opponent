from typing import Any
from flask import Blueprint, render_template, request, abort
from loguru import logger
from sqlalchemy import desc
from werkzeug.exceptions import BadRequest, RequestTimeout
from ast import literal_eval
from opponent_app.models import Product, db, User, Order
from opponent_app.views.product import cache

cart_app = Blueprint("cart_app", __name__)
id: Any = None


@cart_app.route("/<int:cart_id>/", methods=["GET", "POST"])
def cart_list(cart_id: int):
    global id, cart_items
    id = cart_id
    if cart_id is None:
        raise BadRequest(f"Invalid product id #{cart_id}")
    cart = Product.query.filter_by(id=cart_id).one_or_none()
    convert = cache.get("cart")
    if convert is not None:
        cart_items = literal_eval(convert.decode("ascii"))
    else:
        abort(408)
    if request.method == "GET":
        cart.add = True
        db.session.commit()
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        address2 = request.form.get("address2")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip_code")
        user = User(
            email=email,
            phone=phone,
            address=address,
            address2=address2,
            city=city,
            state=state,
            zip_code=int(zip_code),
            full_name=full_name,
        )
        db.session.add(user)
        name_prod = [item.name for item in cart.t_shirts if item.name]
        sex_prod = [item.sex for item in cart.t_shirts if item.sex]
        order = Order(
            color=cart_items[2],
            name_product=name_prod[0],
            order_total=cart_items[4],
            print=cart_items[0][13:],
            quantity=cart_items[1],
            sex=sex_prod[0],
            size=cart_items[3],
        )
        order.users.append(user)
        db.session.add(order)
        db.session.commit()
        order_user = {'Full name: ': full_name, 'Email: ': email, 'Phone: ': phone, 'Address: ': address, 'Address2: ': address2, 'City: ': city, 'State: ': state, 'Zip code: ': zip_code}
        count_orders = Order.query.count()
        cache.setex(name='user_order_count', time=100, value=count_orders)
        cache.setex(name='user_order_phone', time=100, value=phone)
        cache.setex(name='user_order_full_name', time=100, value=full_name)
        return render_template(
            "order/index.html",
            orders_user=order_user,
            product=cart,
            cart_items=cart_items,
            order=str(count_orders).rjust(7, "0"),
        )
    return render_template("cart/index.html", product=cart, cart_items=cart_items)


@cart_app.route("/")
def empty_list(id_cart=None):
    id_cart = id
    if id_cart is None:
        return render_template("cart/empty.html")
    else:
        return cart_list(id_cart)



@cart_app.errorhandler(408)
def handle_request_timeout_error(exception):
    logger.info(exception)
    return render_template('408.html'), 408
