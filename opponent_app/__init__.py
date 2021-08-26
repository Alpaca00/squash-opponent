import sys
from flask import (
    Flask,
    render_template,
    g,
    request,
    url_for,
    redirect,
    current_app,
    abort,
)
from loguru import logger
from opponent_app.config import configurations, mail_settings
from opponent_app.extensions import (
    login_manager,
    security,
    migrate,
    login,
    bootstrap,
    mail,
    babel,
)
from opponent_app.models import db, user_datastore, UserAccount
from opponent_app.views import (
    product_app,
    gallery_app,
    video_app,
    cart_app,
    login_app,
    register_app,
    support_app,
    user_account_app,
    home_app,
    admin,
    about_app,
    finder_app,
    recovery_password_app,
)


def create_app(environment_name="development"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    security.init_app(app, user_datastore)
    bootstrap.init_app(app)
    babel.init_app(app)
    app.config.update(mail_settings)
    mail.init_app(app)
    admin.init_app(app)

    @babel.localeselector
    def get_locale():
        if not g.get("lang_code", None):
            g.lang_code = request.accept_languages.best_match(app.config["LANGUAGES"])
        return g.lang_code

    logger.add(
        sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
    )

    @app.errorhandler(500)
    def handle_internal_server_error(exception):
        logger.info(exception)
        return render_template("500.html"), 500

    app.register_blueprint(home_app, url_prefix="/<lang_code>")
    app.register_blueprint(product_app, url_prefix="/<lang_code>/products")
    app.register_blueprint(gallery_app, url_prefix="/<lang_code>/gallery")
    app.register_blueprint(video_app, url_prefix="/<lang_code>/video")
    app.register_blueprint(cart_app, url_prefix="/<lang_code>/cart")
    app.register_blueprint(login_app, url_prefix="/<lang_code>/login")
    app.register_blueprint(register_app, url_prefix="/<lang_code>/register")
    app.register_blueprint(support_app, url_prefix="/<lang_code>/support")
    app.register_blueprint(user_account_app, url_prefix="/<lang_code>/account")
    app.register_blueprint(about_app, url_prefix="/<lang_code>/about")
    app.register_blueprint(finder_app, url_prefix="/<lang_code>/finder")
    app.register_blueprint(recovery_password_app, url_prefix="/<lang_code>/recovery-password")

    @app.route("/")
    def home():
        g.lang_code = request.accept_languages.best_match(app.config["LANGUAGES"])
        return redirect(url_for("home_app.index"))

    return app


import opponent_app.views
