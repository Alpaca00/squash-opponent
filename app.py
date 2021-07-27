from flask import Flask, request, render_template, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
import config
from views import product_app, gallery_app, video_gallery_app, cart_app, login_app, register_app, support_app
from models import db, TableResult, TableScore

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        table_result = TableResult.query.order_by(TableResult.position).all()
        table_score = TableScore.query.order_by(desc(TableScore.date)).all()
        return render_template("base.html", result=table_result, score=table_score)
    name = "World"
    if request.method == 'POST':
        name = request.form.get('name', 'World')
    return render_template("base.html", name=name)
