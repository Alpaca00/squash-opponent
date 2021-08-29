from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_user
from flask_security.utils import verify_password
from flask_babel import gettext
from opponent_app.models import UserAccount


login_app = Blueprint("login_app", __name__)


@login_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@login_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = UserAccount.query.filter_by(email=email).one_or_none()
        if user_data is not None:
            if verify_password(password=password, password_hash=user_data.password):
                login_user(user_data)
                return redirect(url_for("user_account_app.user_account"))
            else:
                flash_message("Invalid password.")
        else:
            flash_message("Invalid email.")
    return render_template("login/index.html")


def flash_message(text):
    flash(gettext(text))
    return render_template("login/index.html")
