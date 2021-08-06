import pytest
from sqlalchemy import desc
from opponent_app import db, create_app
from opponent_app.models.support import SupportMessage
from tests.locators.support_locators import SupportLocators




SUPPORT = SupportLocators()
QUESTION = "TEST QUESTION"
EMAIL = "lvivsquashteam@gmail.com"
SUBJECT = "TEST SUBJECT"
TEXT = "TEST TEXT"


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def clean_support_db(app):
    yield
    with app.app_context():
        message = SupportMessage.query.order_by(desc(SupportMessage.id)).first()
        db.session.delete(message)
        db.session.commit()


@pytest.mark.support
def test_can_user_send_message_to_support(user, clean_support_db):
    user.open("/support").element(SUPPORT.question_field).type(QUESTION).element(
        SUPPORT.email_field
    ).type(EMAIL).element(SUPPORT.subject_field).type(SUBJECT).element(
        SUPPORT.text_field
    ).type(
        TEXT
    ).element(
        SUPPORT.btn_submit
    ).click()
    assert user.driver.title == 'Home'
