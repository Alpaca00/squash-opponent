from flask import Flask, request, render_template, jsonify
from flask_migrate import Migrate
import config
from views import product_app, gallery_app, video_gallery_app, cart_app
from models import db

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.register_blueprint(product_app, url_prefix='/products')
app.register_blueprint(gallery_app, url_prefix='/gallery')
app.register_blueprint(video_gallery_app, url_prefix='/video_gallery')
app.register_blueprint(cart_app, url_prefix='/cart')

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=['GET', 'POST'])
def index():
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
