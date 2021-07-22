from flask import Blueprint, render_template, request
from werkzeug.exceptions import BadRequest
from models import Product, db

cart_app = Blueprint("cart_app", __name__)


# @cart_app.route("/<int:cart_id>/", methods=['GET', 'POST'])
# def cart_list(cart_id: int):
#     if cart_id is None:
#         raise BadRequest(f"Invalid product id #{cart_id}")
#     cart = Product.query.filter_by(id=cart_id).one_or_none()
#     if request.method == 'GET':
#         cart.add = True
#         db.session.commit()
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         address = request.form.get('address')
#         address2 = request.form.get('address2')
#         city = request.form.get('city')
#         state = request.form.get('state')
#         zip_code = request.form.get('zip_code')
#         user = User(first_name=first_name, last_name=last_name,
#                     email=email, phone=phone, address=address,
#                     address2=address2, city=city, state=state,
#                     zip_code=zip_code
#                     )
#         db.session.add(user)
#         db.session.commit()
#         order_user = User.query.filter_by(phone=phone).all()
#         return render_template("order/index.html", orders_user=order_user, product=cart)
#     return render_template("cart/index.html", product=cart)


@cart_app.route("/")
def empty_list():
    return render_template("cart/empty.html")
