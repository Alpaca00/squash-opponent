import os
import re
import sys
from PIL import Image
import io
from flask import Blueprint, render_template, request, flash, g, url_for
from flask_babel import gettext
from loguru import logger
from opponent_app.helpers import mail, mail_settings, Message
from opponent_app import db
from opponent_app.models import Gallery

gallery_app = Blueprint("gallery_app", __name__)


@gallery_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@gallery_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@gallery_app.route("/", methods=["GET", "POST"])
def gallery_list():
    files = handle_image()
    return render_template("gallery/index.html", files=files)


@gallery_app.route("/upload", methods=["GET", "POST"])
def upload_photo():
    if request.method == "POST":
        img = request.files["input-file-photo"]
        if validate_image(img.filename):
            new_photo = Gallery(name=img.filename, data=img.read())
            db.session.add(new_photo)
            db.session.commit()
            images = Gallery.query.filter_by(name=img.filename).first()
            img = Image.open(io.BytesIO(images.data))
            img.save(f"opponent_app/static/img/user_photo/{images.name}")
            flash(gettext("Successful. Will soon appear in the gallery."))
            subject = "The user uploaded new photos from squash court to our gallery."
            send_info_about_gallery(subject=subject, body=f"Verify {images.name}")
            return render_template("gallery/index.html")
        else:
            flash(gettext("File does not match a format"))
            return render_template("gallery/index.html")


def handle_image():
    directory_img = "opponent_app/static/img/user_photo"
    if os.path.exists(directory_img):
        files = os.listdir(directory_img)
        return files


def validate_image(file_name):
    file_size = sys.getsizeof(file_name)
    if (
        re.findall("([-\w]+\.(?:jpg|gif|png))", file_name)
        and file_size != 0
        or file_size < 150000
    ):
        return True


def send_info_about_gallery(subject, body):
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=["squashopponent@gmail.com"],
        body=body,
    )
    return mail.send(msg)


@gallery_app.errorhandler(408)
def handle_request_timeout_error(exception):
    logger.info(exception)
    return render_template("408.html"), 408


@gallery_app.errorhandler(404)
def handle_not_found_error(exception):
    logger.info(exception)
    return render_template("404.html"), 404


@gallery_app.errorhandler(403)
def handle_resource_is_forbidden_error(exception):
    logger.info(exception)
    return render_template("403.html"), 403
