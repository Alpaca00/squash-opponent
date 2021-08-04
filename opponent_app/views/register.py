from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_security.utils import hash_password
from opponent_app.models.form import RegisterForm
from opponent_app.models import db, user_datastore, UserAccount
from opponent_app.views.validate_form_registration import ValidateForm, ValidationFormError

register_app = Blueprint("register_app", __name__)


@register_app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user_unique_email = UserAccount.query.filter_by(email=form.email.data).one_or_none()
    if request.method == 'GET':
        return render_template("login/register.html", form=form)
    try:
        if ValidateForm(name=form.name.data, email=form.email.data, password=form.password.data):
            if user_unique_email is not None:
                flash('The email is already registered.')
                return render_template("login/register.html", form=form)
            if request.method == 'POST':
                user_datastore.create_user(
                    email=request.form.get('email'),
                    name=request.form.get('name'),
                    password=hash_password(request.form.get('password')),
                )
                db.session.commit()
                flash('Thanks for registering')
                return redirect(url_for('login_app.login'))
    except ValidationFormError as err:
        flash(f'{err}')
        return render_template("login/register.html", form=form)


