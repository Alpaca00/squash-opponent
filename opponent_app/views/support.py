from flask import Blueprint, g, redirect, render_template, request, url_for

from opponent_app.helpers import Message, mail, mail_settings
from opponent_app.models import db
from opponent_app.models.support import SupportMessage

support_app = Blueprint("support_app", __name__)


@support_app.url_defaults
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@support_app.url_value_preprocessor
def pull_lang_code(endpoint, values) -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@support_app.route("/", methods=["GET", "POST", "HEAD"])
def support_list():
    """Render support page."""
    if request.method == "POST":
        question = request.form.get("question")
        email = request.form.get("email")
        subject = request.form.get("subject")
        text = request.form.get("text")
        message = SupportMessage(
            question=question, email=email, subject=subject, text=text
        )
        db.session.add(message)
        db.session.commit()
        send_support_data(
            subject=subject,
            body=f"email: {email}\nquestion: {question}\nmessage: {text}",
        )
        return redirect(url_for("home_app.index"))
    return render_template("support/index.html")


def send_support_data(subject, body):
    """Send support data.

    :param subject: subject
    :param body: body
    """

    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=["squashopponent@gmail.com"],
        body=body,
    )
    return mail.send(msg)
