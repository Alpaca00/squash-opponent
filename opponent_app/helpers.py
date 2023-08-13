import os
from flask_mail import Message
import redis as db
from ast import literal_eval
from werkzeug.exceptions import abort

from opponent_app import mail_settings, mail

REDIS_HOST = os.environ.get("R_HOST")

try:
    redis = db.Redis(host='redis', port=6379, db=0)
except db.exceptions.ConnectionError:
    raise abort(408)


def send_order(subject, body) -> None:
    """Send order data.

    :param subject: subject
    :param body: body
    """
    msg = Message(
        subject=subject,
        sender=mail_settings.get("MAIL_USERNAME"),
        recipients=["squashopponent@gmail.com"],
        body=body,
    )
    mail.send(msg)


def send_order_data_to_user_email():
    """Send order data to user email."""
    try:
        count = redis.get("user_order_count")
        phone_number = redis.get("user_order_phone")
        fullname = redis.get("user_order_full_name")
    except db.ConnectionError as err_redis:
        return err_redis
    except TypeError:
        return None
    else:
        if count and phone_number and fullname is not None:
            order_number = literal_eval(count.decode("ascii"))
            phone = literal_eval(phone_number.decode("ascii"))
            full_name = fullname.decode("ascii")
            return send_order(
                subject="New order",
                body=f"Order: {order_number}, Name: {full_name}, Phone: {phone}",
            )
    finally:
        redis.delete("user_order_count")
        redis.delete("user_order_phone")
        redis.delete("user_order_full_name")
