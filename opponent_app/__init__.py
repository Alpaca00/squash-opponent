import sys
from typing import Literal

from flask import Flask, g, redirect, render_template, request, url_for
from loguru import logger

from opponent_app.config import configurations, mail_settings
from opponent_app.extensions import (
    babel,
    bootstrap,
    login,
    login_manager,
    mail,
    migrate,
    security,
)
from opponent_app.models import (
    OfferOpponent,
    QueueOpponent,
    UserAccount,
    UserOpponent,
    db,
    user_datastore,
)
from opponent_app.public_api import (
    create_publication_api,
    get_all_publications_api,
    get_all_tournaments_api,
    get_user_publications_api,
    health_api,
)
from opponent_app.views import (
    about_app,
    admin,
    cart_app,
    finder_app,
    gallery_app,
    home_app,
    login_app,
    product_app,
    recovery_password_app,
    register_app,
    support_app,
    user_account_app,
    video_app,
)


def create_app(
    environment_name: Literal[
        "production", "development", "testing"
    ] = "production"
) -> Flask:
    """Create a Flask application using the app factory pattern.

    :param environment_name: The name of the environment to use.
    :return: A Flask application.
    """
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
    def get_locale() -> str:
        """Get the language code from the request header."""
        if not g.get("lang_code", None):
            g.lang_code = request.accept_languages.best_match(
                app.config["LANGUAGES"]
            )
        return g.lang_code

    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter="my_module",
        level="INFO",
    )

    @app.errorhandler(500)
    def handle_internal_server_error(exception):  # noqa
        """Handle internal server errors."""
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
    app.register_blueprint(
        recovery_password_app, url_prefix="/<lang_code>/recovery-password"
    )
    app.register_blueprint(health_api, url_prefix="/api/v1/check-health")
    app.register_blueprint(
        get_user_publications_api, url_prefix="/api/v1/get-user-publications"
    )
    app.register_blueprint(
        get_all_publications_api, url_prefix="/api/v1/get-all-publications"
    )
    app.register_blueprint(
        get_all_tournaments_api, url_prefix="/api/v1/get-all-tournaments"
    )
    app.register_blueprint(
        create_publication_api, url_prefix="/api/v1/create-publication"
    )

    @app.route("/")
    def home():
        """Redirect to the home page."""
        g.lang_code = request.accept_languages.best_match(app.config["LANGUAGES"])
        return redirect(url_for("home_app.index"))

    return app


import opponent_app.views  # noqa
