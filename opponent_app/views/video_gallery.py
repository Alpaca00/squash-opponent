from flask import Blueprint, render_template, request, flash

from opponent_app import db
from opponent_app.models.video_gallery import VideoGallery

video_app = Blueprint("video_app", __name__)


@video_app.route("/")
def video_list():
    return render_template("video_gallery/index.html")


@video_app.route("/upload", methods=["POST", "GET"])
def upload_link():
    if request.method == "POST":
        link = request.form.get("video-link")
        new_link = VideoGallery(name=get_name_file(link), link=link)
        db.session.add(new_link)
        db.session.commit()
        flash("Successful. Will soon appear in the gallery.")
        return render_template("video_gallery/index.html")


def get_name_file(file: str):
    if file.startswith('http://') or file.startswith('https://'):
        return 'Valid'
    else:
        return 'Not_valid'

