from unittest import mock
from flask_mail import Message
from opponent_app.extensions import mail
from opponent_app import create_app


def test_send_email_from_app():
    msg = Message(
        subject="test",
        sender=create_app().config.get("MAIL_USERNAME"),
        recipients=["lvivsquashteam@gmail.com"],
        body="simple test99",
    )
    with mock.patch(
        "opponent_app.extensions.mail.send", return_value=msg
    ) as mocked_mail:
        with create_app().app_context():
            test = mail.send(msg)
            mocked_mail.assert_called_once_with(test)
            mocked_mail.assert_called()


def test_send_data_to_web_site_email():
    msg = [{"subject": "test title", "body": "test data"}]
    with mock.patch(
        "opponent_app.extensions.mail.send_message", return_value=msg
    ) as mocked_mail:
        with create_app().app_context():
            message = mail.send_message(
                subject="test title",
                body="test data",
            )
            assert len(message) == 1
            assert message[0]["subject"] == "test title"
            assert message[0]["body"] == "test data"
