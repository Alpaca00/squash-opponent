from flask import request, render_template, redirect, url_for, flash, Blueprint, g, current_app, abort, Response
from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_babel import refresh
from flask_login import current_user, login_user, logout_user
from flask_security.utils import verify_password
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
from loguru import logger
from opponent_app.extensions import login_manager
from opponent_app.helpers import send_order_data_to_user_email
from opponent_app import babel
from opponent_app.models import (
    UserAccount,
    TableResult,
    TableScore,
    AdminLoginForm,
    User,
    db,
)
from opponent_app.models.basic_queries.junior_result import (
    juniors_up_to_9,
    juniors_up_to_11,
    juniors_up_to_13,
    juniors_up_to_15,
)
from opponent_app.models.support import SupportMessage


home_app = Blueprint("home_app", __name__)


@home_app.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@home_app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@home_app.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        abort(404)


@login_manager.user_loader
def load_user(user_id):
    logger.info("The user is load.")
    return UserAccount.query.get(int(user_id))


@home_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        table_result = TableResult.query.order_by(TableResult.position).all()
        table_score = TableScore.query.order_by(desc(TableScore.date)).all()
        send_order_data_to_user_email()
        return render_template(
            "base.html",
            result=table_result,
            score=table_score,
            juniors_up_to_9=juniors_up_to_9,
            juniors_up_to_11=juniors_up_to_11,
            juniors_up_to_13=juniors_up_to_13,
            juniors_up_to_15=juniors_up_to_15,
        )
    if request.method == "POST":  # todo: fix or remove this method
        email = request.form.get("email")
        password = request.form.get("password")
        user_login = UserAccount.query.filter_by(email=email).one_or_none()
        if user_login.password == password:
            user = user_login.name
            return render_template("base.html", user=user)


@home_app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            name = request.form.get("username")
            password = request.form.get("password")
            remember = True if request.form.get("remember") else False
            admin_ = UserAccount.query.filter_by(name=name).first()
            if admin_:
                if (
                    verify_password(password=password, password_hash=admin_.password)
                    and name == "admin"
                ):
                    login_user(admin_, remember=remember)
                    logger.info(current_user.name)
                    if current_user.is_authenticated:
                        logger.info("Admin role.")
                        return redirect(url_for("admin.index"))
                else:
                    flash("Invalid username or password.")
                    return redirect(url_for("home_app.login_admin"))
    return render_template("admin/login_index.html", form=form)


@home_app.errorhandler(408)
def handle_request_timeout_error(exception):
    logger.info(exception)
    return render_template("408.html"), 408


@home_app.errorhandler(404)
def handle_not_found_error(exception):
    logger.info(exception)
    return render_template("404.html"), 404


@home_app.errorhandler(403)
def handle_resource_is_forbidden_error(exception):
    logger.info(exception)
    return render_template("403.html"), 403



class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login_admin"))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            logger.info(
                f"The current user is authenticated: {current_user.is_authenticated}"
            )
            return current_user.is_authenticated
        else:
            return handle_resource_is_forbidden_error(Exception)


admin = Admin(name="Admin", template_mode="bootstrap4", index_view=MyAdminIndexView())
admin.add_view(MyModelView(UserAccount, db.session))


class FinderOpponentView(BaseView):
    @expose("/")
    def index(self):
        opponents = UserAccount.query.all()
        return self.render(
            "admin/finder_opponent/index.html", user=current_user, opponents=opponents
        )

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(FinderOpponentView(name="Finder-Opponent", endpoint="opponent"))


class SupportView(BaseView):
    @expose("/")
    def index(self):
        supports = SupportMessage.query.order_by("id").all()
        return self.render("admin/support/index.html", support=supports)

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(SupportView(name="Support", endpoint="support"))


class CustomersView(BaseView):
    @expose("/")
    def index(self):
        customer = User.query.order_by("id").all()
        return self.render("admin/customers/index.html", customer=customer)

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(CustomersView(name="Customers", endpoint="customers/"))


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logger.info("The admin is logged out.")
        logout_user()
        return redirect(url_for("home_app.login_admin"))

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(LogoutView(name="Logout", endpoint="logout"))
