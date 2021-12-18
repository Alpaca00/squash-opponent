import pytest
from flask import url_for


USERNAME = 'Not_Admin'
PASSWORD = 'qwerty12345'


@pytest.mark.apps
def test_home_app(client):
    response = client.get("/")
    assert "Home" and "Lviv Squash Team" in str(response.data)
    assert response.status_code == 200


@pytest.mark.apps
def test_admin_page_index(client):
    response = client.get(url_for("admin.index"))
    assert response.status_code == 200


@pytest.mark.apps
def test_admin_login(client, auth):
    res1 = client.get(url_for("home_app.login_admin"))
    assert res1.status_code == 200
    auth.login(
        url="home_app.login_admin", username=USERNAME, password=PASSWORD
        )
    res2 = client.get(url_for("admin.index"))
    assert res2.status_code == 200
    with client:
        res3 = client.get("/admin/")
        assert isinstance(res3, Exception)
