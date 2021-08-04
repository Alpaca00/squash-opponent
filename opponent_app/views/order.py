from flask import Blueprint, render_template


order_app = Blueprint("order_app", __name__)


@order_app.route("/")
def order_list():
    return render_template("order/index.html")

