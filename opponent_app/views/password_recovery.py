from flask import Blueprint, render_template, request, url_for, redirect, flash, g
from flask_security.utils import hash_password
from opponent_app.models import db, user_datastore, UserAccount
from opponent_app.helpers import mail, mail_settings, Message


recovery_password_app = Blueprint("recovery_password_app", __name__)


@recovery_password_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@recovery_password_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@recovery_password_app.route("/", methods=["GET", "POST"])
def password_recovery():
    if request.method == "POST":
        email = request.form.get("email")
        user = UserAccount.query.filter_by(email=email).one_or_none()
        if user is not None:
            personal_info = user.password  # fix hash
            html = render_template('login/mail_recovery_psw.html', personal_info=personal_info)
            subject = "Squash Opponent account recovery."
            send_info_by_user(subject=subject, recipient=user.email, template=html)
            flash("Your password has been sent to the mail.")
            return redirect( url_for("login_app.login"))
    return render_template("login/password_recovery.html")


def send_info_by_user(subject, recipient, template):
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=[recipient],
        html=template,
    )
    return mail.send(msg)
