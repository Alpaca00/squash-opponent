from datetime import datetime
import calendar
import humanize
from flask import request, Blueprint, render_template, g, redirect, url_for
from opponent_app.models import UserAccount, UserOpponent, OfferOpponent, db

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
                    ]
                )
        offer_data = []
        dates2 = []
        offer_opponent = OfferOpponent.query.all()
        if offer_opponent is not None:
            for i in offer_opponent:
                convert_dt = datetime.strptime(i.offer_date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())

                dates2.append(
                    [
                        abr_month,
                        day_,
                        time_,
                        i.offer_city,
                        i.offer_district,
                        i.offer_category,
                        i.offer_phone,
                        i.user_opponent_id,
                        i.offer_accept,
                    ]
                )

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
            "finder/index.html",
            opponents=opponents,
            dates=dates,
            offer_data=offer_data,
            dates2=dates2,
        )
    if request.method == "POST":
        phone = request.form.get("user_phone")
        name = request.form.get("user_name")
        email = request.form.get("user_email")
        category = request.form.get("user_category")
        district = request.form.get("user_district")
        date = request.form.get("user_partydate")
        opponent_id = request.form.get("opponent_id_user")
        offer_opponent = OfferOpponent(
            offer_phone=phone,
            offer_name=name,
            offer_email=email,
            offer_category=category,
            offer_city="Lviv",
            offer_district=district,
            offer_date=date,
            user_opponent_id=opponent_id,
        )
        db.session.add(offer_opponent)
        db.session.commit()
        return redirect(url_for("finder_app.index"))
    return redirect(url_for("finder_app.index"))


# for delete outdated posts
def time_feed():
    def generate():
        yield datetime.now().strftime("%H:%M:%S")

    return generate()
