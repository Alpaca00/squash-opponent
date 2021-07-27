from flask import Blueprint, render_template, request
from models import UserAccount

login_app = Blueprint("login_app", __name__)


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_login = UserAccount.query.filter_by(email=email).one_or_none()
        if user_login.password == password:
            user = user_login.name
            return render_template("base.html", user=user)
        else:
            return render_template("login/index.html")
    return render_template("login/index.html")

