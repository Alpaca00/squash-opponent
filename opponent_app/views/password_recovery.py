import random
import string

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask_babel import gettext
from flask_security.utils import hash_password

from opponent_app.helpers import Message, mail, mail_settings, redis
from opponent_app.models import UserAccount, db

recovery_password_app = Blueprint("recovery_password_app", __name__)


@recovery_password_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@recovery_password_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@recovery_password_app.route("/", methods=["GET", "POST"])
def password_recovery():
    """Render password recovery page."""
    if request.method == "POST":
        email = request.form.get("email")
        user = UserAccount.query.filter_by(email=email).one_or_none()
        if user is not None:
            generate_hash = "".join(
                random.choices(string.ascii_letters + string.digits, k=24)
            )
            redis.setex(name="User_Security_Code", time=900, value=generate_hash)
            html = render_template(
                "login/mail_recovery_psw.html", personal_info=generate_hash
            )
            subject = "Squash Opponent account recovery."
            send_info_by_user(
                subject=subject, recipient=user.email, template=html
            )
            flash(gettext("Security code has been sent to the mail."))
            return redirect(url_for("recovery_password_app.recover", email=email))
        else:
            flash("Invalid email.")
    return render_template("login/password_recovery.html")


@recovery_password_app.route("/recover/<email>", methods=["GET", "POST"])
def recover(email):
    """Render recover page.

    :param email: user email
    """
    try:
        security_code = redis.get("User_Security_Code")
        if security_code is None:
            redis.delete("User_Security_Code")
            return redirect(url_for("recovery_password_app.password_recovery"))
    except redis.ConnectionError as err_redis:
        return err_redis
    else:
        if request.method == "POST":
            code = request.form.get("code")
            if code == security_code.decode("ascii"):
                return redirect(
                    url_for("recovery_password_app.change_password", email=email)
                )
            else:
                flash(gettext("Wrong security code."))
                redis.delete("User_Security_Code")
    return render_template("login/recover.html")


@recovery_password_app.route(
    "/recover/<email>/change_password", methods=["GET", "POST"]
)
def change_password(email):
    """Render change password page.

    :param email: user email
    """
    if request.method == "POST":
        user = UserAccount.query.filter_by(email=email).one_or_none()
        if user is not None:
            new_password = request.form.get("password")
            password_confirm = request.form.get("password_confirm")
            if new_password == password_confirm:
                user.password = hash_password(new_password)
                db.session.commit()
                flash(gettext("Your password has been changed."))
                html = render_template("login/mail_password_changed.html")
                send_info_by_user(
                    subject="Your password has been changed.",
                    recipient=email,
                    template=html,
                )
                return redirect(url_for("login_app.login"))
        else:
            flash(gettext("Something went wrong."))
            redis.delete("User_Security_Code")
            return render_template("login/recover.html")
    return render_template("login/new_password.html")


def send_info_by_user(subject, recipient, template):
    """Send email to user.

    :param subject: email subject
    :param recipient: email recipient
    :param template: email template
    """
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=[recipient],
        html=template,
    )
    return mail.send(msg)
