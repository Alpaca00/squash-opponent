from itsdangerous import URLSafeTimedSerializer
from opponent_app import current_app


def generate_confirmation_token(email):
    """Generate confirmation token.

    :param email: email
    :return: token
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    """Confirm token.

    :param token: token
    :param expiration: expiration
    :return: email
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except Exception:  # noqa
        return False
    return email
