from datetime import datetime
import calendar
import humanize
from flask import request, Blueprint, render_template, g
from opponent_app.models import UserAccount, UserOpponent

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
                convert_dt = datetime.strptime(i.date, "%Y-%m-%dT%H:%M")
                abr_month = calendar.month_abbr[int(convert_dt.date().month)]
                day_ = humanize.naturaldate(convert_dt.day)
                time_ = humanize.naturaltime(convert_dt.time())
                dates.append(
                    [abr_month, day_, time_, i.city, i.district, i.category, i.phone]
                )
        return render_template("finder/index.html", opponents=opponents, dates=dates)


# for delete outdated posts
def time_feed():
    def generate():
        yield datetime.now().strftime("%H:%M:%S")

    return generate()
