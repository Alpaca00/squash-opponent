from flask import Blueprint, render_template, request, jsonify, abort
from loguru import logger
from werkzeug.exceptions import BadRequest
import redis
from opponent_app.models import Product, db

product_app = Blueprint("product_app", __name__)

cache = redis.Redis()


def sep_data(lst):
    res = [item.split(",") for item in lst]
    return res[0][::-1]


@product_app.route("/")
def product_list():
    product = Product.query.filter_by(deleted=False).order_by(Product.id).all()
    return render_template("products/index.html", products=product)


@product_app.route("/<int:product_id>/", methods=['GET', 'DELETE', 'POST'])
def product_detail(product_id: int):
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None:
        abort(404)
    if request.method == "POST":
        res = request.values
        data = sep_data(res)
        cache.setex(name='cart', time=3600, value=str(data[0:5]))
    if request.method == "DELETE":
        product.deleted = True
        db.session.commit()
        return jsonify(ok=True)
    return render_template(
        "products/detail.html",
        product=product,
    )


@product_app.errorhandler(408)
def handle_request_timeout_error(exception):
    logger.info(exception)
    return render_template('408.html'), 408


@product_app.errorhandler(404)
def handle_not_found_error(exception):
    logger.info(exception)
    return render_template('404.html'), 404
