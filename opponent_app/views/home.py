from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_babel import gettext
from flask_login import current_user, login_user, logout_user
from flask_security.utils import verify_password
from loguru import logger
from sqlalchemy import desc

from opponent_app.extensions import login_manager
# from opponent_app.helpers import send_order_data_to_user_email
from opponent_app.models import (
    AdminLoginForm,
    TableResult,
    TableScore,
    User,
    UserAccount,
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
def add_language_code(endpoint, values) -> None:  # noqa
    """Add language code to url.

    :param endpoint: endpoint name
    :param values: url values
    """
    values.setdefault("lang_code", g.lang_code)


@home_app.url_value_preprocessor
def pull_lang_code(endpoint, values)  -> None:  # noqa
    """Pull language code from url.

    :param endpoint: endpoint name
    :param values: url values
    """
    g.lang_code = values.pop("lang_code")


@home_app.before_request
def before_request():
    """Check if language code is valid."""
    if g.lang_code not in current_app.config["LANGUAGES"]:
        abort(404)


@login_manager.user_loader
def load_user(user_id) -> UserAccount:
    """Load user by id."""
    logger.info("The user is load.")
    return UserAccount.query.get(int(user_id))


@home_app.route("/", methods=["GET", "POST"])
def index():
    """Render home page."""
    if request.method == "GET":
        table_result = TableResult.query.order_by(TableResult.position).all()
        table_score = TableScore.query.order_by(desc(TableScore.date)).all()
        # todo: fix email sending
        # send_order_data_to_user_email()
        return render_template(
            "base.html",
            result=table_result,
            score=table_score,
            juniors_up_to_9=juniors_up_to_9,
            juniors_up_to_11=juniors_up_to_11,
            juniors_up_to_13=juniors_up_to_13,
            juniors_up_to_15=juniors_up_to_15,
        )
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_login = UserAccount.query.filter_by(email=email).one_or_none()
        if user_login.password == password:
            user = user_login.name
            return render_template("base.html", user=user)


@home_app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    """Render admin login page."""
    form = AdminLoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            name = request.form.get("username")
            password = request.form.get("password")
            remember = True if request.form.get("remember") else False
            admin_ = UserAccount.query.filter_by(name=name).first()
            if admin_:
                if (
                    verify_password(
                        password=password, password_hash=admin_.password
                    )
                    and name == "admin"
                ):
                    login_user(admin_, remember=remember)
                    logger.info(current_user.name)
                    if current_user.is_authenticated:
                        logger.info("Admin role.")
                        return redirect(url_for("admin.index"))
                else:
                    flash(gettext("Invalid username or password."))
                    return redirect(url_for("home_app.login_admin"))
    return render_template("admin/login_index.html", form=form)


@home_app.errorhandler(408)
def handle_request_timeout_error(exception):
    """Handle request timeout error."""
    logger.info(exception)
    return render_template("408.html"), 408


@home_app.errorhandler(404)
def handle_not_found_error(exception):
    """Handle not found error."""
    logger.info(exception)
    return render_template("404.html"), 404


@home_app.errorhandler(403)
def handle_resource_is_forbidden_error(exception):
    """Handle resource is forbidden error."""
    logger.info(exception)
    return render_template("403.html"), 403


class MyModelView(ModelView):
    """Customized model view."""

    def is_accessible(self):
        """Check if user is authenticated."""
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if user is not authenticated."""
        return redirect(url_for("login_admin"))


class MyAdminIndexView(AdminIndexView):
    """Customized admin index view."""
    def is_accessible(self):
        """Check if user is authenticated."""
        if current_user.is_authenticated:
            logger.info(
                f"The current user is authenticated: {current_user.is_authenticated}"
            )
            return current_user.is_authenticated
        else:
            return handle_resource_is_forbidden_error(Exception)


admin = Admin(
    name="Admin", template_mode="bootstrap4", index_view=MyAdminIndexView()
)
admin.add_view(MyModelView(UserAccount, db.session))


class FinderOpponentView(BaseView):
    """Customized finder opponent view."""
    @expose("/")
    def index(self):
        """Render finder opponent page."""
        opponents = UserAccount.query.all()
        return self.render(
            "admin/finder_opponent/index.html",
            user=current_user,
            opponents=opponents,
        )

    def is_accessible(self):
        """Check if user is authenticated."""
        return current_user.is_authenticated


admin.add_view(FinderOpponentView(name="Finder-Opponent", endpoint="opponent"))


class SupportView(BaseView):
    """Customized support view."""
    @expose("/")
    def index(self):
        """Render support page."""
        supports = SupportMessage.query.order_by("id").all()
        return self.render("admin/support/index.html", support=supports)

    def is_accessible(self):
        """Check if user is authenticated."""
        return current_user.is_authenticated


admin.add_view(SupportView(name="Support", endpoint="support"))


class CustomersView(BaseView):
    """Customized customers view."""
    @expose("/")
    def index(self):
        """Render customers page."""
        customer = User.query.order_by("id").all()
        return self.render("admin/customers/index.html", customer=customer)

    def is_accessible(self):
        """Check if user is authenticated."""
        return current_user.is_authenticated


admin.add_view(CustomersView(name="Customers", endpoint="customers/"))


class LogoutView(BaseView):
    """Customized logout view."""
    @expose("/")
    def index(self):
        """Render logout page."""
        logger.info("The admin is logged out.")
        logout_user()
        return redirect(url_for("home_app.login_admin"))

    def is_accessible(self):
        """Check if user is authenticated."""
        return current_user.is_authenticated


admin.add_view(LogoutView(name="Logout", endpoint="logout"))
