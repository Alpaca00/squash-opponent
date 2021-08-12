from datetime import datetime
from flask import request, Blueprint, render_template, g
from opponent_app.models import UserAccount, UserOpponent

finder_app = Blueprint("finder_app", __name__)


@finder_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@finder_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@finder_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        opponents = UserAccount.query.join(UserOpponent).all()
        for x in opponents:
            for i in x.users_opponent:
                print(i.category)
        return render_template('finder/index.html', opponents=opponents)


# for delete outdated posts
def time_feed():
    def generate():
        yield datetime.now().strftime("%H:%M:%S")
    return generate()
