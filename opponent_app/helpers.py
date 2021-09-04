import os
from flask_mail import Message
import redis as db
from ast import literal_eval
from werkzeug.exceptions import abort

from opponent_app import mail_settings, mail

R_HOST = os.environ.get("R_HOST")

try:
    # r = db.Redis(host='redis', port=6379, db=0)  # prod
    r = db.Redis()  # dev
except db.exceptions.ConnectionError:
    raise abort(408)


def send_order(subject, body):
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=["squashopponent@gmail.com"],
        body=body,
    )
    mail.send(msg)


def send_order_data_to_user_email():
    try:
        c = r.get("user_order_count")
        p = r.get("user_order_phone")
        f = r.get("user_order_full_name")
    except db.ConnectionError as err_redis:
        return err_redis
    except TypeError:
        return None
    else:
        if c and p and f is not None:
            order_number = literal_eval(c.decode("ascii"))
            phone = literal_eval(p.decode("ascii"))
            full_name = f.decode("ascii")
            return send_order(
                subject="New order",
                body=f"Order: {order_number}, Name: {full_name}, Phone: {phone}",
            )
    finally:
        r.delete("user_order_count")
        r.delete("user_order_phone")
        r.delete("user_order_full_name")
