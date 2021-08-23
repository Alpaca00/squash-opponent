import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash, g
from flask_login import login_required, login_user, current_user
from flask_security.utils import hash_password
from opponent_app.models.form import RegisterForm
from opponent_app.models import db, user_datastore, UserAccount
from opponent_app.views.validate_form_registration import (
    ValidateForm,
    ValidationFormError,
)
from opponent_app.helpers import mail, mail_settings, Message
from opponent_app.token import generate_confirmation_token, confirm_token


register_app = Blueprint("register_app", __name__)


@register_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", g.lang_code)


@register_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop("lang_code")


@register_app.route("/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    user_unique_email = UserAccount.query.filter_by(email=form.email.data).one_or_none()
    if request.method == "GET":
        return render_template("login/register.html", form=form)
    try:
        if ValidateForm(
            name=form.name.data, email=form.email.data, password=form.password.data
        ):
            if user_unique_email is not None:
                flash("The email is already registered.")
                return render_template("login/register.html", form=form)
            if request.method == "POST":
                user_datastore.create_user(
                    email=request.form.get("email"),
                    name=request.form.get("name"),
                    password=hash_password(request.form.get("password")),
                    registered_on=datetime.datetime.now(),
                    confirmed=False,
                )
                db.session.commit()
                user = UserAccount.query.filter_by(email=form.email.data).first_or_404()
                token = generate_confirmation_token(user.email)

                confirm_url = url_for('register_app.confirm_email', token=token, _external=True)
                html = render_template('gmail.html', confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_info_by_user(recipient=user.email, subject=subject, template=html)
                login_user(user)
                flash("Thanks for registering")
                return redirect(url_for("register_app.unconfirmed"))
    except ValidationFormError as err:
        flash(f"{err}")
        return render_template("login/register.html", form=form)


@register_app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    else:
        user = UserAccount.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('home_app.index'))


@register_app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('home_app.index')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')


@register_app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('register_app.confirm_email', token=token, _external=True)
    html = render_template('gmail.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_info_by_user(recipient=current_user.email, subject=subject, template=html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('register_app.unconfirmed'))


def send_info_by_user(subject, recipient, template):
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=[recipient],
        html=template,
    )
    return mail.send(msg)


@register_app.errorhandler(404)
def handle_not_found_error(exception):
    return render_template("404.html"), 404
