from flask import Blueprint, render_template, request, url_for, redirect
from flask_security.utils import hash_password
from form import RegisterForm
from models import db, user_datastore

register_app = Blueprint("register_app", __name__)


@register_app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return "The form has been submitted. Success!"
    if request.method == 'POST':
        user_datastore.create_user(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_password(request.form.get('password')),
        )
        db.session.commit()
        return redirect(url_for('login_app.login'))
    return render_template("login/register.html", form=form)

