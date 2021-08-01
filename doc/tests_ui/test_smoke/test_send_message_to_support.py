import pytest
from sqlalchemy import desc
from doc.locators.support_locators import SupportLocators
from app import SupportMessage, db, app

SUPPORT = SupportLocators()
QUESTION = "TEST QUESTION"
EMAIL = "lvivsquashteam@gmail.com"
SUBJECT = "TEST SUBJECT"
TEXT = "TEST TEXT"


@pytest.fixture
def clean_support_db():
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
