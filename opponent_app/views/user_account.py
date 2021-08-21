import calendar
from datetime import datetime
import humanize
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    g,
    redirect,
    abort,
    flash,
)
from flask_babel import gettext
from flask_login import current_user, logout_user, login_required
from loguru import logger
from opponent_app.models import db, UserOpponent, UserAccount, OfferOpponent

user_account_app = Blueprint("user_account_app", __name__)


@user_account_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@user_account_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@user_account_app.route("/", methods=["GET", "POST"])
def user_account():
    if request.method == "GET":
        user_history = (
            UserAccount.query.filter_by(id=current_user.id).join(UserOpponent).all()
        )
        lst_history = []
        for x in user_history:
            for i in x.users_opponent:
                convert_dt = datetime.strptime(i.opponent_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                lst_history.append(
                    [
                        abr_month,
                        day_,
                        time_,
                        i.opponent_city,
                        i.opponent_district,
                        i.opponent_category,
                        i.opponent_phone,
                        i.id,
                    ]
                )
        offer_data = []
        offer_id = []
        offer_opponent = OfferOpponent.query.join(UserOpponent).all()
        if offer_opponent is not None:
            for i in offer_opponent:
                convert_dt = datetime.strptime(i.offer_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                offer_id.append(i.offer_accept)
                offer_data.append(
                    [
                        abr_month,
                        day_,
                        time_,
                        i.offer_phone,
                        i.offer_name,
                        i.offer_email,
                        i.offer_city,
                        i.offer_district,
                        i.offer_category,
                        i.offer_phone,
                        i.user_opponent_id,
                        i.id,
                        i.offer_accept,
                    ]
                )
        return render_template(
            "user.html",
            cur=current_user,
            opponents=user_history,
            dates=lst_history,
            offer_data=offer_data,
            offer_id=offer_id,
            offer_opponent=offer_opponent,
        )
    if request.method == "POST":
        date_time = request.form.get("partydate")
        category = request.form.get("category")
        district = request.form.get("district")
        phone = request.form.get("phone")
        opponent = UserOpponent(
            opponent_category=category,
            opponent_city="Lviv",
            opponent_district=district,
            opponent_phone=phone,
            opponent_date=date_time,
            user_account_id=current_user.id,
        )
        db.session.add(opponent)
        db.session.commit()
        flash(gettext("Successfully. Your post has been added."))
        return redirect(url_for("user_account_app.user_account"))
    return render_template("user.html", cur=current_user)


@user_account_app.route("/update/<post_id>", methods=["GET", "POST", "DELETE"])
def update_post_request(post_id: int):
    if request.method == "POST":
        card_opponent = (
            UserOpponent.query.filter_by(id=post_id).join(UserAccount).one_or_none()
        )
        if card_opponent is None:
            abort(404)
        else:
            card_opponent.opponent_phone = request.form.get("phone")
            card_opponent.opponent_category = request.form.get("category")
            card_opponent.opponent_district = request.form.get("district")
            card_opponent.opponent_date = request.form.get("partydate")
            db.session.commit()
            return redirect(url_for("user_account_app.user_account"))
    if request.method == "GET":
        card_opponent = (
            UserOpponent.query.filter_by(id=post_id).join(UserAccount).one_or_none()
        )
        if card_opponent is None:
            abort(404)
        else:
            return render_template(
                "user_update.html",
                cur=current_user,
                post_id=post_id,
                phone=card_opponent.opponent_phone,
                category=card_opponent.opponent_category,
                district=card_opponent.opponent_district,
                date=card_opponent.opponent_date,
            )
         # send_list_to_mail
    return render_template("user_update.html", cur=current_user, post_id=post_id)


@user_account_app.route("/delete/<post_id>", methods=["GET", "POST", "DELETE"])
def delete_post_request(post_id: int):
    if request.method == "GET":
        card_opponent_for_delete = (
            UserOpponent.query.filter_by(id=post_id).join(UserAccount).one_or_none()
        )
        card_offer = (
            OfferOpponent.query.filter_by(user_opponent_id=post_id).one_or_none()
        )
        if card_opponent_for_delete is None and card_offer is None:
            abort(404)
        else:
            db.session.delete(card_opponent_for_delete)
            db.session.delete(card_offer)
            db.session.commit()
            flash(gettext("Successfully. Your post has been deleted."))
             # send_list_to_mail
        return redirect(url_for("user_account_app.user_account"))
    return render_template("user.html", cur=current_user)


@user_account_app.route("/cancel/<post_id>", methods=["GET", "POST", "DELETE"])
def cancel_post_offer(post_id: int):
    if request.method == "GET":
        offer_opponent = OfferOpponent.query.filter_by(id=post_id).one_or_none()
        if offer_opponent is None:
            abort(404)
        else:
            db.session.delete(offer_opponent)
            db.session.commit()
            flash(gettext("Successfully. The offer has been deleted."))
            # send_list_to_mail
        return redirect(url_for("user_account_app.user_account"))
    return render_template("user.html", cur=current_user)


@user_account_app.route("/accept/<post_id>", methods=["GET", "POST", "DELETE"])
def accept_post_offer(post_id: int):
    if request.method == "GET":
        offer_opponent = OfferOpponent.query.filter_by(id=post_id).one_or_none()
        if offer_opponent is None:
            abort(404)
        else:
            if not offer_opponent.offer_accept:
                offer_opponent.offer_accept = True
                db.session.commit()
                flash(gettext("Successfully. The offer has been accepted."))
                 # send_list_to_mail
                return redirect(url_for("user_account_app.user_account"))
    return render_template("user.html", cur=current_user)


@user_account_app.errorhandler(404)
def handle_not_found_error(exception):
    logger.info(exception)
    return render_template("404.html"), 404


@user_account_app.route("/login", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "GET":
        logout_user()
        return redirect(url_for("login_app.login"))
