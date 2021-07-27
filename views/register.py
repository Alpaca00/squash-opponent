from flask import Blueprint, render_template, request
from form import RegisterForm
from models import UserAccount, db

register_app = Blueprint("register_app", __name__)



@register_app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return "the form has been submitted. Success!"
    if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        password = form.password.data
        user_account = UserAccount(email=email, name=name, password=password)
        db.session.add(user_account)
        db.session.commit()
        return render_template("login/index.html")
    return render_template("login/register.html", form=form)
