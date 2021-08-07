from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from flask_security.utils import verify_password
from opponent_app.models import UserAccount


login_app = Blueprint("login_app", __name__)


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = UserAccount.query.filter_by(email=email).one_or_none()
        if user_data is not None:
            if verify_password(password=password, password_hash=user_data.password):
                login_user(user_data)
                return redirect(url_for('user_account_app.user_account'))
            else:
                flash_message("Invalid password.")
        else:
            flash_message("Invalid email.")
    return render_template("login/index.html")


def flash_message(text):
    flash(text)
    return render_template("login/index.html")

# @login_app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     logger.info(e)
    #     return render_template('400.html', reason=e.description), 400
