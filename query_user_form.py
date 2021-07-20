from flask import request

from models import db, User
from app import app


# @app.route("/cart/<string:first_name&last_name&email&phone&address&address2&city&state&zip_code/")
# def insert_data(first_name, last_name,
#                 email, phone, address,
#                 address2, city, state,
#                 zip_code
# ):
#     with app.app_context():
#         user = User(first_name=first_name, last_name=last_name,
#                     email=email, phone=phone, address=address,
#                     address2=address2, city=city, state=state,
#                     zip_code=zip_code
#                     )
#         db.session.add(user)
#         db.session.commit()

@app.route("/cart/<string:first_name>/")
def insert_data(first_name):
    username = request.args.get('first_name')
    print(username)
    return f"<h1>Hello {username}!</h1>"
