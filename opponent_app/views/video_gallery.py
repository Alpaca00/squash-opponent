from flask import Blueprint, render_template


video_app = Blueprint("video_app", __name__)


@video_app.route("/")
def video_list():
    return render_template("video_gallery/index.html")
