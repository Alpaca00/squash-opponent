from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_babel import gettext
from flask_login import login_user
from flask_security.utils import verify_password
from loguru import logger

from opponent_app.models import UserAccount

login_app = Blueprint("login_app", __name__)


@login_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@login_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    """Render login page."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = (
            UserAccount.query.filter_by(email=email)
            .group_by(UserAccount.id)
            .one_or_none()
        )
        if user_data is not None:
            if verify_password(
                password=password, password_hash=user_data.password
            ):
                login_user(user_data)
                return redirect(url_for("user_account_app.user_account"))
            else:
                flash_message("Invalid password.")
        else:
            flash_message("Invalid email.")
    return render_template("login/index.html")


def flash_message(text) -> render_template:
    """Flash message.

    :param text: text to flash
    """
    flash(gettext(text))
    return render_template("login/index.html")


@login_app.errorhandler(408)
def handle_request_timeout_error(exception):
    """Handle request timeout error."""
    logger.info(exception)
    return render_template("408.html"), 408


@login_app.errorhandler(404)
def handle_not_found_error(exception):
    """Handle not found error."""
    logger.info(exception)
    return render_template("404.html"), 404


@login_app.errorhandler(403)
def handle_resource_is_forbidden_error(exception):
    """Handle resource is forbidden error."""
    logger.info(exception)
    return render_template("403.html"), 403
