import sys
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required, LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
from loguru import logger
import redis
from ast import literal_eval
import config
from views import product_app, gallery_app, video_gallery_app, cart_app, login_app, register_app, support_app, user_account_app
from models import db, TableResult, TableScore, UserAccount, AdminLogin, user_datastore


app = Flask(__name__)


app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SPS']
app.config['SECRET_KEY'] = '6Lf0rL8bAAAAAL0YqesYius-y0iQnYThoR-RWd0s'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'public'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'private'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}


app.register_blueprint(product_app, url_prefix='/products')
app.register_blueprint(gallery_app, url_prefix='/gallery')
app.register_blueprint(video_gallery_app, url_prefix='/video_gallery')
app.register_blueprint(cart_app, url_prefix='/cart')
app.register_blueprint(login_app, url_prefix='/login')
app.register_blueprint(register_app, url_prefix='/register')
app.register_blueprint(support_app, url_prefix='/support')
app.register_blueprint(user_account_app, url_prefix='/account')

db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
security = Security(app, user_datastore)
login_manager = LoginManager()
login_manager.init_app(app)



logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)
r = redis.Redis()


def messenger(subject, body):
    with app.app_context():
        msg = Message(subject=subject,
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["lvivsquashteam@gmail.com"],
                      body=body)
        mail.send(msg)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        table_result = TableResult.query.order_by(TableResult.position).all()
        table_score = TableScore.query.order_by(desc(TableScore.date)).all()
        send_email()
        return render_template("base.html", result=table_result, score=table_score)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_login = UserAccount.query.filter_by(email=email).one_or_none()
        if user_login.password == password:
            user = user_login.name
            return render_template("base.html", user=user)


def send_email():
    try:
        c = r.get("user_order_count")
        p = r.get("user_order_phone")
        f = r.get("user_order_full_name")
    except redis.ConnectionError as err_redis:
        return err_redis
    else:
        if c and p and f is not None:
            order_number = literal_eval(c.decode("ascii"))
            phone = literal_eval(p.decode("ascii"))
            full_name = f.decode("ascii")
            return messenger(
                subject="new_order",
                body=f"Order: {order_number}, name: {full_name}, phone: {phone}",
            )


@login.user_loader
def load_user(user_id):
    return AdminLogin.query.get(user_id)


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are now logged out"


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_admin'))


# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated


admin = Admin(app, template_mode='bootstrap4')
admin.add_view(MyModelView(AdminLogin, db.session))


@app.route('/admin/login')
def login_admin():
    admin_login = AdminLogin.query.get(1)
    login_user(admin_login)
    return "Logged in!"


@app.route('/admin/logout')
def logout_admin():
    logout_user()
    return "Logged out!"


# class DashboardView(AdminIndexView):
#
#     @expose('/')
#     def index(self):
#         return self.render('admin/dashboard_index.html')



# class FinderOpponentView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/finder_opponent/index.html')
#
#
# admin.add_view(FinderOpponentView(name='Finder-Opponent', endpoint='opponent'))


# class SenderView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/sender/index.html')
#
#
# admin.add_view(SenderView(name='Sender', endpoint='sender'))
#
#
# class CustomersView(BaseView):
#
#     @expose('/')
#     def index(self, uid: int = 1):
#
#         customer = "John Doe"
#         orders = 1
#         stats = 'None'
#
#         return self.render('admin/customers/index.html', customer=customer, orders=orders, stats=stats)
#
#
# admin.add_view(CustomersView(name='Customers', endpoint='customers/'))


