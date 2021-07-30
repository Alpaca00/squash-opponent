from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from flask_security.utils import verify_password
from models import UserAccount


login_app = Blueprint("login_app", __name__)


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_login = UserAccount.query.filter_by(email=email).one_or_none()
        if verify_password(password=password, password_hash=user_login.password):
            login_user(user_login)
            return redirect(url_for('user_account_app.user_account'))
        else:
            return render_template("login/index.html")
    return render_template("login/index.html")

