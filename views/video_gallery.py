from flask import Blueprint, render_template


video_gallery_app = Blueprint("video_gallery_app", __name__)


@video_gallery_app.route("/")
def video_gallery_list():
    return render_template("video_gallery/index.html")
