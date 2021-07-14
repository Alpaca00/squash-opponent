from flask import Flask, request, render_template
from flask_migrate import Migrate
import config
from views import product_app, gallery_app, video_gallery_app
from models import db

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
)
app.register_blueprint(product_app, url_prefix='/products')
app.register_blueprint(gallery_app, url_prefix='/gallery')
app.register_blueprint(video_gallery_app, url_prefix='/video_gallery')

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=['GET', 'POST'])
def index():
    name = "World"
    if request.method == 'POST':
        name = request.form.get('name', 'World')
    return render_template("base.html", name=name)


@app.route("/hello/<string:name>/")
def home(name=None):
    if name is None:
        name = 'World!'
    return f"<h1>Hello {name}!</h1>"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'
