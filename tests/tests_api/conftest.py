import pytest
from flask import url_for
from opponent_app import create_app, db
import os
import tempfile


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app("test")
    with app.app_context():
        db.init_app(app)
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, url, username, password):
        return self._client.post(
            url_for(url),
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/admin/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
