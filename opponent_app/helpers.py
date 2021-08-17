import os
from flask_mail import Message
import redis
from ast import literal_eval
from opponent_app import mail_settings, mail


R_HOST = os.environ['R_HOST']

r = redis.Redis(host=R_HOST)


def admin_messenger(subject, body):
    msg = Message(subject=subject,
                  sender=mail_settings.get("MAIL_USERNAME"),
                  recipients=["lvivsquashteam@gmail.com"],
                  body=body
                  )
    mail.send(msg)


def send_order_data_to_user_email():
    try:
        c = r.get("user_order_count")
        p = r.get("user_order_phone")
        f = r.get("user_order_full_name")
    except redis.ConnectionError as err_redis:
        return err_redis
    else:
        if c and p and f is not None:
            order_number = literal_eval(c.decode("ascii"))
            phone = literal_eval(p.decode("ascii"))
            full_name = f.decode("ascii")
            return admin_messenger(
                subject="New order",
                body=f"Order: {order_number}, Name: {full_name}, Phone: {phone}",
            )
    finally:
        r.delete("user_order_count")
        r.delete("user_order_phone")
        r.delete("user_order_full_name")
