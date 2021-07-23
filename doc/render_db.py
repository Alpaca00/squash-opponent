from jinja2 import Template
from app import app
from models import db, User, Product


def my_function():
    with app.app_context():
        user = User.query.all()
        return iter(user)


s = "{% for user in users %} {{loop.index}} {% endfor %}"
a = Template(s).render(users=my_function())
print(a)


