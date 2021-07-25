from flask import Blueprint, render_template, request

login_app = Blueprint("login_app", __name__)


@login_app.route("/", methods=["GET", "POST", "HEAD"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
        return render_template("base.html")
    return render_template("login/index.html")


