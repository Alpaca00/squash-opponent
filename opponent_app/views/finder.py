import calendar
from datetime import datetime, timedelta
from typing import Optional

import humanize
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from flask_babel import gettext
from loguru import logger

from opponent_app.models import (
    Member,
    OfferOpponent,
    QueueOpponent,
    UserAccount,
    UserMember,
    UserOpponent,
    db,
)
from opponent_app.views.common import render_content_tournaments

finder_app = Blueprint("finder_app", __name__)


@finder_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@finder_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


def prepare_opponent_data(opponents) -> list:
    """Prepare opponent data for rendering.

    :param opponents: opponents from db
    :return: list of opponents
    """
    dates = []
    for opponent in opponents:
        for user_opponent in opponent.users_opponent:
            convert_dt = datetime.strptime(
                user_opponent.opponent_date, "%Y-%m-%dT%H:%M"
            )
            abr_month = calendar.month_abbr[int(convert_dt.date().month)]
            day_ = humanize.naturaldate(convert_dt.day)
            time_ = humanize.naturaltime(convert_dt.time())
            dates.append(
                [
                    abr_month,
                    day_,
                    time_,
                    user_opponent.opponent_city,
                    user_opponent.opponent_district,
                    user_opponent.opponent_category,
                    user_opponent.opponent_phone,
                    user_opponent.id,
                    opponent.name,
                    opponent.email,
                    opponent.count,
                ]
            )
    return dates


def add_queue_size(dates) -> None:
    """Add queue size to opponent data.

    :param dates: opponent data
    """
    for date in dates:
        queue_opponent = (
            UserOpponent.query.join(OfferOpponent)
            .filter_by(user_opponent_id=int(date[7]))
            .join(QueueOpponent)
            .all()
        )
        size = (
            len(queue_opponent) + 1
            if len(queue_opponent) >= 1
            else len(queue_opponent)
        )
        date.append(size)


def prepare_offer_data(offer_opponents) -> list:
    """Prepare offer data for rendering.

    :param offer_opponents: offer opponents from db
    :return: list of offer opponents
    """
    offer_data = []
    for offer in offer_opponents:
        convert_dt = datetime.strptime(offer.offer_date, "%Y-%m-%dT%H:%M")
        abr_month = calendar.month_abbr[int(convert_dt.date().month)]
        day_ = humanize.naturaldate(convert_dt.day)
        time_ = humanize.naturaltime(convert_dt.time())
        offer_data.append(
            [
                abr_month,
                day_,
                time_,
                offer.offer_phone,
                offer.offer_name,
                offer.offer_email,
                offer.offer_city,
                offer.offer_district,
                offer.offer_category,
                offer.offer_phone,
                offer.user_opponent_id,
                offer.id,
                offer.offer_accept,
                offer.offer_message,
            ]
        )
    return offer_data


@finder_app.route("/", methods=["GET", "POST"])
def index():
    """Render index page."""
    if request.method == "GET":
        perform_auto_remove_old_posts()

        opponents = (
            UserAccount.query.join(UserOpponent).group_by(UserAccount.id).all()
        )
        dates = prepare_opponent_data(opponents)
        add_queue_size(dates)

        offer_opponents = OfferOpponent.query.all()
        offer_data = prepare_offer_data(offer_opponents)

        return render_template(
            "finder/index.html",
            opponents=opponents,
            dates=dates,
            offer_data=offer_data,
        )

    if request.method == "POST":
        post_offer()

    return redirect(url_for("finder_app.index"))


def post_offer() -> redirect:
    """Post offer."""
    id_offer = request.form.get("hidden-id-offer")
    phone = request.form.get("user_phone")
    name = request.form.get("user_name")
    email = request.form.get("user_email")
    category = request.form.get("user_category")
    district = request.form.get("user_district")
    date = request.form.get("user_partydate")  # e.g. 2021-05-20T12:00  # noqa
    message = request.form.get("user_message_text")
    opponent_id = request.form.get("opponent_id_user")

    if id_offer == "":
        offer_opponent = OfferOpponent(
            offer_phone=phone,
            offer_name=name,
            offer_email=email,
            offer_category=category,
            offer_city="Lviv",  # TODO: add city to form
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
            flash(
                "You need to wait for the answer of the opponent on the last offer."
            )

    db.session.commit()
    return redirect(url_for("finder_app.index"))


def query_opponent_for_search() -> list:
    """Query opponent for search."""
    opponent = UserAccount.query.join(UserOpponent).all()
    return opponent


def query_offer_for_search() -> list:
    """Query offer for search."""
    offer = OfferOpponent.query.all()
    return offer


def search_render(
    opponent_search: Optional[str] = None, offer_search: Optional[str] = None
):  # -> render_template | redirect:
    """Search render.

    :param opponent_search: opponent search
    :param offer_search: offer search

    :return: render template or redirect
    """
    opponents = opponent_search
    if opponents is None:
        opponents = query_opponent_for_search()
    dates = []
    for opponent in opponents:
        for data in opponent.users_opponent:
            convert_dt = datetime.strptime(data.opponent_date, "%Y-%m-%dT%H:%M")
            abr_month = calendar.month_abbr[int(convert_dt.date().month)]
            day_ = humanize.naturaldate(convert_dt.day)
            time_ = humanize.naturaltime(convert_dt.time())
            dates.append(
                [
                    abr_month,
                    day_,
                    time_,
                    data.opponent_city,
                    data.opponent_district,
                    data.opponent_category,
                    data.opponent_phone,
                    data.id,
                    opponent.name,
                    opponent.email,
                    opponent.count,
                ]
            )
        offer_data = []
        offer_opponent = offer_search
        if offer_opponent is None:
            offer_opponent = query_offer_for_search()
        if offer_opponent:
            for data in offer_opponent:
                convert_dt = datetime.strptime(data.offer_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                offer_data.append(
                    [
                        abr_month,
                        day_,
                        time_,
                        data.offer_phone,
                        data.offer_name,
                        data.offer_email,
                        data.offer_city,
                        data.offer_district,
                        data.offer_category,
                        data.offer_phone,
                        data.user_opponent_id,
                        data.id,
                        data.offer_accept,
                        data.offer_message,
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
    """Flash message for query.

    :param for_size_query: for size query, default None

    :return: flash message
    """
    if for_size_query is not None:
        size = len(for_size_query)
        if int(size) == 1:
            return flash(f"{size} - opponent found.")
        else:
            return flash(f"{size} - opponents found.")


@finder_app.route("/search", methods=["GET", "POST"])
def search():
    """Search query for opponent."""
    if request.method == "GET":
        text_search = request.args.get("search")
        by_name = UserAccount.query.filter(
            UserAccount.name.contains(text_search)  # noqa
        ).all()
        by_email = UserAccount.query.filter(
            UserAccount.email.contains(text_search)  # noqa
        ).all()
        by_category_opponent = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_category.contains(text_search))  # noqa
            .all()
        )
        by_opponent_district = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_district.contains(text_search))  # noqa
            .all()
        )
        by_opponent_phone = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_phone.contains(text_search))  # noqa
            .all()
        )
        by_opponent_date = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_date.contains(text_search))  # noqa
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
    """Search query for opponent by category."""
    if request.method == "GET":
        query_category = request.args
        text_search = list(map(str, query_category))[0].upper()
        by_category_opponent = (
            UserAccount.query.join(UserOpponent)
            .filter(UserOpponent.opponent_category.contains(text_search))  # noqa
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


@finder_app.route("/tournaments/", methods=["GET", "POST"])
def render_tournaments():
    """Render tournaments."""
    if request.method == "GET":
        tournaments_history = UserMember.query.join(Member).all()
        query = db.session.query(Member.user_member_id).all()
        return render_content_tournaments(
            tournaments_history, "finder/tournaments_content.html", query
        )
    if request.method == "POST":
        tournament_id = request.form.get("hidden-id-offer")
        phone = request.form.get("user_phone")
        name = request.form.get("user_name")
        email = request.form.get("user_email")
        if tournament_id != "" and phone != "" and name != "" and email != "":
            member_join = Member(
                user_member_id=tournament_id,
                tour_member_name=name,
                tour_member_phone=phone,
                tour_member_email=email,
            )
            db.session.add(member_join)
            db.session.commit()
            flash(
                gettext(
                    "You will be able to join the tournament after confirming the organizer."
                )
            )
            return redirect(url_for("finder_app.render_tournaments"))
        else:
            abort(404)
    return render_template("finder/tournaments_content.html")


def perform_auto_remove_old_posts() -> None:
    """Perform auto remove old posts from queue."""
    dt = datetime.today() - timedelta(days=1)
    card_opponent = (
        UserOpponent.query.filter(
            UserOpponent.opponent_date.contains(str(dt.date()))  # noqa
        )
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
                logger.info(f"Removed queue_opponent.")
            if card_offer:
                db.session.delete(card_offer)
                db.session.commit()
                logger.info(f"Removed offer_opponent.")
            if card_opponent:
                db.session.delete(card_opponent[n])
                db.session.commit()
                logger.info(f"Removed post_opponent.")


@finder_app.errorhandler(404)
def handle_not_found_error(exception):
    """Handle not found error."""
    logger.info(exception)
    return render_template("404.html"), 404
