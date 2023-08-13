from flask import Blueprint, g, render_template

order_app = Blueprint("order_app", __name__)


@order_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@order_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@order_app.route("/")
def order_list():
    """Render order page."""
    return render_template("order/index.html")
