import sys
from flask import Flask, render_template
from loguru import logger
from opponent_app.config import configurations, mail_settings
from opponent_app.extensions import (login_manager, security,
                                     migrate, login, bootstrap, mail
                                     )
from opponent_app.models import db, user_datastore, UserAccount
from opponent_app.views import (product_app, gallery_app,
                                video_app, cart_app,
                                login_app, register_app,
                                support_app, user_account_app, home_app,
                                admin, about_app
                                )


def create_app(environment_name='development'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    security.init_app(app, user_datastore)
    bootstrap.init_app(app)
    # csrf.init_app(app)
    app.config.update(mail_settings)
    mail.init_app(app)
    admin.init_app(app)

    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

    @app.errorhandler(500)
    def handle_internal_server_error(exception):
        logger.info(exception)
        return render_template('500.html'), 500

    app.register_blueprint(home_app, url_prefix='/')
    app.register_blueprint(product_app, url_prefix='/products')
    app.register_blueprint(gallery_app, url_prefix='/gallery')
    app.register_blueprint(video_app, url_prefix='/video')
    app.register_blueprint(cart_app, url_prefix='/cart')
    app.register_blueprint(login_app, url_prefix='/login')
    app.register_blueprint(register_app, url_prefix='/register')
    app.register_blueprint(support_app, url_prefix='/support')
    app.register_blueprint(user_account_app, url_prefix='/account')
    app.register_blueprint(about_app, url_prefix='/about')

    return app


import opponent_app.views
