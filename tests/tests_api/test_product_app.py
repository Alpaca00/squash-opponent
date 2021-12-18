from flask import url_for


def test_product_app(client):
    response = client.get(url_for("product_app.product_list"))
    assert b"MAN T-shirt with our print" in response.data
