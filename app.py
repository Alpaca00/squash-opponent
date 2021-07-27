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
        table_score = TableScore.query.order_by(TableScore.date).all()
        return render_template("base.html", result=table_result, score=table_score)
    name = "World"
    if request.method == 'POST':
        name = request.form.get('name', 'World')
    return render_template("base.html", name=name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    print(post_id)
    return f'Post {post_id}'

#
# @app.route('/cart/<string:first_name>')
# def show_data():
#     first_name = request.form.get('first_name')
#     print(first_name)
#     return render_template("base.html")

#
# @app.route('/cart', methods=['GET', 'POST'])
# def form_to_json():
#     data = request.form.to_dict(flat=False)
#     # return jsonify(data)
#     return '''<h1>The language value is: {}</h1>
#                   <h1>The framework value is: {}</h1>'''.format(data)
#
#
# @app.route('/cart/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
# def form_example():
#     if request.method == 'POST':  #this block is only entered when the form is submitted
#         language = request.form.get('language')
#         framework = request.form['framework']
#         print(language)
#         print(framework)
#         return '''<h1>The language value is: {}</h1>
#                   <h1>The framework value is: {}</h1>'''.format(language, framework)
#
#     return '''<form method="POST">
#                   Language: <input type="text" name="language"><br>
#                   Framework: <input type="text" name="framework"><br>
#                   <input type="submit" value="Submit"><br>
#               </form>'''
