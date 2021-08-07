from flask import Blueprint, render_template, request
from sqlalchemy import desc
from opponent_app.models import db, TableResult, TableScore
from opponent_app.models.support import SupportMessage

support_app = Blueprint("support_app", __name__)


@support_app.route("/", methods=["GET", "POST", "HEAD"])
def support_list():
    if request.method == "POST":
        table_result = TableResult.query.order_by(TableResult.position).all()
        table_score = TableScore.query.order_by(desc(TableScore.date)).all()
        question = request.form.get("question")
        email = request.form.get("email")
        subject = request.form.get("subject")
        text = request.form.get("text")
        message = SupportMessage(
            question=question, email=email, subject=subject, text=text
        )
        db.session.add(message)
        db.session.commit()
        return render_template("base.html", result=table_result, score=table_score)
    return render_template("support/index.html")
