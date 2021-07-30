from flask import Blueprint, render_template
from flask_login import current_user


user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.route("/", methods=["GET", "POST"])
def user_account():
    return render_template("user.html", cur=current_user)

