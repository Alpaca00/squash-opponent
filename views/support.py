from flask import Blueprint, render_template, request

from models import db
from models.support import SupportMessage

support_app = Blueprint("support_app", __name__)


@support_app.route("/", methods=["GET", "POST", "HEAD"])
def support_list():
    if request.method == "POST":
        question = request.form.get('question')
        email = request.form.get('email')
        subject = request.form.get('subject')
        text = request.form.get('text')
        message = SupportMessage(question=question, email=email, subject=subject, text=text)
        db.session.add(message)
        db.session.commit()
        return render_template("base.html")
    return render_template("support/index.html")
