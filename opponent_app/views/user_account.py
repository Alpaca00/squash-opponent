from flask import Blueprint, render_template, jsonify, request, url_for, g
from flask_login import current_user, logout_user, login_required
from werkzeug.utils import redirect
from opponent_app.models import db, UserOpponent

user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@user_account_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@user_account_app.route("/", methods=["GET", "POST"])
def user_account():
    if request.method == "POST":
        date_time = request.form.get("partydate")
        category = request.form.get("category")
        district = request.form.get("district")
        phone = request.form.get("phone")
        opponent = UserOpponent(
            category=category, city='Lviv',
            district=district, phone=phone,
            date=date_time, user_account_id=current_user.id
        )
        db.session.add(opponent)
        db.session.commit()
        return render_template("user.html", cur=current_user)
    return render_template("user.html", cur=current_user)



@user_account_app.route('/login', methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return redirect(url_for('login_app.login'))
