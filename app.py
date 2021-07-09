from flask import Flask, request
from views import product_app


app = Flask(__name__)
app.register_blueprint(product_app, url_prefix='/products')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return f"<h1>Hello {request.form.get('name', 'World!')}</h1>"
    return "<h1>Hello world!</h1>"


@app.route("/hello/<string:name>/")
def home(name=None):
    if name is None:
        name = 'World!'
    return f"<h1>Hello {name}!</h1>"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'
