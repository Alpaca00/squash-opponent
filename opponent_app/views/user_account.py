from flask import Blueprint, render_template, jsonify, request, url_for
from flask_login import current_user, logout_user, login_required
from werkzeug.utils import redirect

user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.route("/", methods=["GET", "POST"])
def user_account():
    return render_template("user.html", cur=current_user)


@user_account_app.route('/login', methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return redirect(url_for('login_app.login'))
