import redis
from flask import Blueprint, abort, g, jsonify, make_response, render_template, request
from loguru import logger

from opponent_app.models import Product, db

product_app = Blueprint("product_app", __name__)

cache = redis.Redis()


def separate_data(product_data: any):
    """Separate data from redis.

    :param product_data: data from redis
    """
    try:
        result = [item.split(",") for item in product_data]
        if not result:
            return "Exception: Empty list"
        return result[0][::-1]
    except IndexError:
        return "Exception: Index out of range"


@product_app.url_defaults
def add_language_code(endpoint, values)  -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@product_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@product_app.route("/")
def product_list():
    """Render product page."""
    product = Product.query.filter_by(deleted=False).order_by(Product.id).all()
    return render_template("products/index.html", products=product)


@product_app.route("/<int:product_id>/", methods=["GET", "DELETE", "POST"])
def product_detail(product_id: int):
    """Render product detail page.

    :param product_id: product id from url
    """
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None:
        abort(404)
    if request.method == "POST":
        products = request.values
        data = separate_data(products)
        products = make_response("Setting a cookie")
        products.set_cookie(key="cart", value=str(data[0:5]), max_age=None)
        try:
            cache.setex(name="cart", time=300, value=str(data[0:5]))
        except TypeError:
            return "The object is not subscriptable"  # noqa
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
    """Handle request timeout error."""
    logger.info(exception)
    return render_template("408.html"), 408


@product_app.errorhandler(404)
def handle_not_found_error(exception):
    """Handle not found error."""
    logger.info(exception)
    return render_template("404.html"), 404
