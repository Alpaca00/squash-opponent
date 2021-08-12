from flask import Blueprint, render_template, request, flash, g
from flask_babel import gettext
from opponent_app import db
from opponent_app.models.video_gallery import VideoGallery

video_app = Blueprint("video_app", __name__)


@video_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@video_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@video_app.route("/")
def video_list():
    return render_template("video_gallery/index.html")


@video_app.route("/upload", methods=["POST", "GET"])
def upload_link():
    if request.method == "POST":
        link = request.form.get("video-link")
        unique_link = VideoGallery.query.filter_by(link=link).first()
        if unique_link is None:
            new_link = VideoGallery(name=get_name_file(link), link=link)
            db.session.add(new_link)
            db.session.commit()
            flash(gettext("Successful. Will soon appear in the gallery."))
            return render_template("video_gallery/index.html")
        else:
            flash(gettext("Warning. The link is already in our gallery."))
            return render_template("video_gallery/index.html")


def get_name_file(file: str):
    if file.startswith('http://') or file.startswith('https://'):
        return 'Valid'
    else:
        return 'Not_valid'

