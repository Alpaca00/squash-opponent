from flask import Blueprint, render_template, g

order_app = Blueprint("order_app", __name__)


@order_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@order_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@order_app.route("/")
def order_list():
    return render_template("order/index.html")

