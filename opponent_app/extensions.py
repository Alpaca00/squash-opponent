from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security
from flask_bootstrap import Bootstrap
from flask_babel import Babel


login_manager = LoginManager()
mail = Mail()
security = Security()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
babel = Babel()
