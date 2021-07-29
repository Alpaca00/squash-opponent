from flask import Blueprint, render_template, request
from models import UserAccount

user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.route("/<int:user_id>/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def user_account(user_id: int):
    user = UserAccount.query.filter_by(id=user_id).one_or_none()
    if request.method == "POST":
        return render_template("user.html", user=user)
    else:
        return render_template("login/index.html")


@user_account_app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def user_account_active():
    if request.method == "GET":
        return render_template("user.html")
    else:
        return render_template("login/index.html")
