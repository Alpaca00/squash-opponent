from flask_wtf import RecaptchaField, FlaskForm
from wtforms import PasswordField, StringField, validators, BooleanField



class RegisterForm(FlaskForm):
    name = StringField('name', [validators.DataRequired(), validators.Length(max=255)])
    password = PasswordField('new password', [validators.DataRequired(),validators.Length(min=8)])
    email = StringField('emailaddress', [validators.DataRequired(), validators.Length(min=6, max=35)])
    recaptcha = RecaptchaField()


class AdminLoginForm(FlaskForm):
    username = StringField('username', validators=[validators.InputRequired(), validators.Length(min=4, max=15)])
    password = PasswordField('password', validators=[validators.InputRequired(), validators.Length(min=8, max=255)])
    remember = BooleanField('remember me')


