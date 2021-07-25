from flask import Blueprint, render_template, request

register_app = Blueprint("register_app", __name__)


@register_app.route("/", methods=["GET", "POST", "HEAD"])
def register_list():
    return render_template("login/register.html")
