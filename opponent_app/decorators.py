from functools import wraps
from flask import flash, redirect, url_for
from flask_babel import gettext
from flask_login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash(gettext("Warning! Please confirm your account!"))
            return redirect(url_for("register_app.unconfirmed"))
        return func(*args, **kwargs)

    return decorated_function
