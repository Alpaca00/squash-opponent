from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, PasswordField, StringField, validators


class RegisterForm(FlaskForm):
    """Register form."""

    email = StringField(
        "email", [validators.InputRequired(), validators.Length(min=6, max=35)]
    )
    name = StringField(
        "name", [validators.InputRequired(), validators.Length(max=255)]
    )
    password = PasswordField(
        "password", [validators.InputRequired(), validators.Length(min=8)]
    )
    recaptcha = RecaptchaField()


class AdminLoginForm(FlaskForm):
    """Admin login form."""

    username = StringField(
        "username",
        validators=[validators.InputRequired(), validators.Length(min=4, max=15)],
    )
    password = PasswordField(
        "password",
        validators=[
            validators.InputRequired(),
            validators.Length(min=8, max=255),
        ],
    )
    remember = BooleanField("remember me")
