from flask import Blueprint, render_template, request, jsonify
from werkzeug.exceptions import BadRequest
from models import Product

product_app = Blueprint("product_app", __name__)

PRODUCTS = {
    1: 'Smartphone',
    2: 'Tablet',
    3: 'Laptop'
}


@product_app.route("/")
def product_list():
    product = Product.query.all()
    for row in Product.query.all():
        print(row.name, row.is_new)
    return render_template("products/index.html", products=product)


@product_app.route("/<int:product_id>/", methods=['GET', 'DELETE'])
def product_detail(product_id: int):
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None:
        raise BadRequest(f"Invalid product id #{product_id}")
    if request.method == "DELETE":
        PRODUCTS.pop(product_id)
        return jsonify(ok=True)
    return render_template(
        "products/detail.html",
        product=product,
    )


