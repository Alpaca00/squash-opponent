from datetime import datetime, timedelta
import calendar
import humanize
import loguru
from flask import request, Blueprint, render_template, g, redirect, url_for, flash
from flask_babel import gettext
from opponent_app.models import (
    UserAccount,
    UserOpponent,
    OfferOpponent,
    db,
    QueueOpponent,
)

finder_app = Blueprint("finder_app", __name__)


@finder_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@finder_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@finder_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        at_specific_time_to_perform_auto_remove_old_post()
        opponents = UserAccount.query.join(UserOpponent).all()
        dates = []
        for x in opponents:
            for i in x.users_opponent:
                convert_dt = datetime.strptime(i.opponent_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                dates.append(
                    [
                        abr_month,
                        day_,
                        time_,
                        i.opponent_city,
                        i.opponent_district,
                        i.opponent_category,
                        i.opponent_phone,
                        i.id,
                        x.name,
                        x.email,
                        x.count,
                    ]
                )
        offer_data = []
        for x in opponents:
            for i in range(len(x.users_opponent)):
                queue_opponent = (
                    UserOpponent.query.join(OfferOpponent)
                    .filter_by(user_opponent_id=int(dates[i][7]))
                    .join(QueueOpponent)
                    .all()
                )
                size = len(queue_opponent)
                if size >= 1:
                    size += 1
                    dates[i].append(size)
                else:
                    queue_opponent = (
                        UserOpponent.query.join(OfferOpponent)
                        .filter_by(user_opponent_id=int(dates[i][7]))
                        .all()
                    )
                    size = len(queue_opponent)
                    dates[i].append(size)

        offer_opponent = OfferOpponent.query.all()
        if offer_opponent:
            for i in offer_opponent:
                convert_dt = datetime.strptime(i.offer_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
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
                        i.offer_message,
                    ]
                )
        return render_template(
            "finder/index.html",
            opponents=opponents,
            dates=dates,
            offer_data=offer_data,
        )
    if request.method == "POST":
        post_offer()
    return redirect(url_for("finder_app.index"))


def post_offer():
    id_offer = request.form.get("hidden-id-offer")
    phone = request.form.get("user_phone")
    name = request.form.get("user_name")
    email = request.form.get("user_email")
    category = request.form.get("user_category")
    district = request.form.get("user_district")
    date = request.form.get("user_partydate")
    message = request.form.get("user_message_text")
    opponent_id = request.form.get("opponent_id_user")

    if id_offer == "":
        offer_opponent = OfferOpponent(
            offer_phone=phone,
            offer_name=name,
            offer_email=email,
            offer_category=category,
            offer_city="Lviv",
            offer_district=district,
            offer_date=date,
            user_opponent_id=opponent_id,
            offer_message=message,
        )
        db.session.add(offer_opponent)
    else:
        offer_ = (
            OfferOpponent.query.join(UserOpponent)
            .filter_by(id=int(id_offer))
            .join(UserAccount)
            .one_or_none()
        )
        card = (
            QueueOpponent.query.join(OfferOpponent)
            .join(UserOpponent)
            .filter_by(id=int(id_offer))
            .join(UserAccount)
            .one_or_none()
        )
        if offer_ is not None and card is None:
            queue_opponent = QueueOpponent(
                queue_phone=phone,
                queue_name=name,
                queue_email=email,
                queue_category=category,
                queue_city="Lviv",
                queue_district=district,
                queue_date=date,
                queue_offer_opponent_id=int(offer_.id),
                queue_message=message,
            )
            db.session.add(queue_opponent)
        if card is not None:
            flash("You need to wait for the answer of the opponent on the last offer.")

    db.session.commit()
    return redirect(url_for("finder_app.index"))


def query_opponent_for_search():
    opponent = UserAccount.query.join(UserOpponent).all()
    return opponent


def query_offer_for_search():
    offer = OfferOpponent.query.all()
    return offer


def search_render(opponent_search=None, offer_search=None):
    opponents = opponent_search
    if opponents is None:
        opponents = query_opponent_for_search()
    dates = []
    for x in opponents:
        for i in x.users_opponent:
            convert_dt = datetime.strptime(i.opponent_date, "%Y-%m-%dT%H:%M")
            abr_month = calendar.month_abbr[int(convert_dt.date().month)]
            day_ = humanize.naturaldate(convert_dt.day)
            time_ = humanize.naturaltime(convert_dt.time())
            dates.append(
                [
                    abr_month,
                    day_,
                    time_,
                    i.opponent_city,
                    i.opponent_district,
                    i.opponent_category,
                    i.opponent_phone,
                    i.id,
                    x.name,
                    x.email,
                    x.count,
                ]
            )
        offer_data = []
        offer_opponent = offer_search
        if offer_opponent is None:
            offer_opponent = query_offer_for_search()
        if offer_opponent:
            for i in offer_opponent:
                convert_dt = datetime.strptime(i.offer_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
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
                        i.offer_message,
                    ]
                )
        return render_template(
            "finder/index.html",
            opponents=opponents,
            dates=dates,
            offer_data=offer_data,
        )
    return redirect(url_for("finder_app.index"))


def flash_message_for_query(for_size_query: str = None) -> flash:
    if for_size_query is not None:
        size = len(for_size_query)
        if int(size) == 1:
            return flash(f"{size} - opponent found.")
        else:
            return flash(f"{size} - opponents found.")


@finder_app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        text_search = request.args.get("search")
        by_name = UserAccount.query.filter(UserAccount.name.contains(text_search)).all()
        by_email = UserAccount.query.filter(
            UserAccount.email.contains(text_search)
        ).all()
        by_category_opponent = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_category.contains(text_search))
            .all()
        )
        by_opponent_district = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_district.contains(text_search))
            .all()
        )
        by_opponent_phone = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_phone.contains(text_search))
            .all()
        )
        by_opponent_date = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_date.contains(text_search))
            .all()
        )
        if by_name:
            flash_message_for_query(by_name)
            return search_render(opponent_search=by_name)
        elif by_email:
            flash_message_for_query(by_email)
            return search_render(opponent_search=by_email)
        elif by_category_opponent:
            flash_message_for_query(by_category_opponent)
            return search_render(opponent_search=by_category_opponent)
        elif by_opponent_district:
            flash_message_for_query(by_opponent_district)
            return search_render(opponent_search=by_opponent_district)
        elif by_opponent_phone:
            flash_message_for_query(by_opponent_phone)
            return search_render(opponent_search=by_opponent_phone)
        elif by_opponent_date:
            flash_message_for_query(by_opponent_date)
            return search_render(opponent_search=by_opponent_date)
        else:
            flash(gettext("Nothing was found for this query."))
    if request.method == "POST":
        post_offer()
    return redirect(url_for("finder_app.index"))


@finder_app.route("/search_category/", methods=["GET", "POST"])
def search_category():
    if request.method == "GET":
        query_category = request.args
        text_search = list(map(str, query_category))[0].upper()
        by_category_opponent = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_category.contains(text_search))
            .all()
        )
        if by_category_opponent:
            flash_message_for_query(by_category_opponent)
            return search_render(opponent_search=by_category_opponent)
        else:
            flash(gettext("Nothing was found for this query."))
    if request.method == "POST":
        post_offer()
    return redirect(url_for("finder_app.index"))


def at_specific_time_to_perform_auto_remove_old_post():
    dt = datetime.today() - timedelta(days=1)
    card_opponent = (
        UserOpponent.query.filter(UserOpponent.opponent_date.contains(str(dt.date())))
        .join(UserAccount)
        .all()
    )
    quantity_posts = len(card_opponent)
    if quantity_posts >= 1:
        for n in range(quantity_posts):
            card_offer = OfferOpponent.query.filter_by(
                user_opponent_id=card_opponent[n].id
            ).one_or_none()
            queue_opponent = (
                UserOpponent.query.join(OfferOpponent)
                .filter_by(user_opponent_id=card_opponent[n].id)
                .join(QueueOpponent)
                .one_or_none()
            )
            if queue_opponent:
                db.session.delete(queue_opponent)
                db.session.commit()
                loguru.logger.info(f"Removed queue_opponent.")
            if card_offer:
                db.session.delete(card_offer)
                db.session.commit()
                loguru.logger.info(f"Removed offer_opponent.")
            if card_opponent:
                db.session.delete(card_opponent[n])
                db.session.commit()
                loguru.logger.info(f"Removed post_opponent.")
