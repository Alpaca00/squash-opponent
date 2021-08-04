from flask import Blueprint, render_template


gallery_app = Blueprint("gallery_app", __name__)


@gallery_app.route("/")
def gallery_list():
    return render_template("gallery/index.html")
