import calendar
from datetime import datetime
import humanize
from flask import Blueprint, render_template, jsonify, request, url_for, g, redirect, abort
from flask_login import current_user, logout_user, login_required
from loguru import logger

from opponent_app.models import db, UserOpponent, UserAccount

user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@user_account_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@user_account_app.route("/", methods=["GET", "POST"])
def user_account():
    if request.method == "GET":
        user_history = UserAccount.query.filter_by(id=current_user.id).join(UserOpponent).all()
        lst_history = []
        for x in user_history:
            for i in x.users_opponent:
                convert_dt = datetime.strptime(i.date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                lst_history.append(
                    [abr_month, day_, time_, i.city, i.district, i.category, i.phone, i.id]
                )
        return render_template("user.html", cur=current_user, opponents=user_history, dates=lst_history)
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


@user_account_app.route("/update/<post_id>", methods=["GET", "POST", "PATCH"])
def update_post_request(post_id: int):
    if request.method == "POST":
        card_opponent = UserOpponent.query.filter_by(id=post_id).join(UserAccount).one_or_none()
        if card_opponent is None:
            abort(404)
        else:
            # card_opponent.phone = request.form.get('phone')
            # card_opponent.category = request.form.get('category')
            # card_opponent.district = request.form.get("district")
            # card_opponent.date = request.form.get("date")
            # db.session.commit()
            # print(card_opponent.date)
            print(request.form.get("date"))
            return redirect(url_for("user_account_app.user_account"))
    return render_template("user_update.html", cur=current_user, post_id=post_id)


@user_account_app.errorhandler(404)
def handle_not_found_error(exception):
    logger.info(exception)
    return render_template("404.html"), 404


@user_account_app.route('/login', methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return redirect(url_for('login_app.login'))
