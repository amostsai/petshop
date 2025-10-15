from decimal import Decimal
from urllib.parse import urlparse


def test_view_cart_renders_items(client, monkeypatch, sample_cart_summary):
    monkeypatch.setattr("app.features.cart.routes.service.get_summary", lambda: sample_cart_summary)

    response = client.get("/cart/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert sample_cart_summary["items"][0]["name"] in body


def test_add_item_redirects_to_cart(client, monkeypatch, sample_cart_summary):
    calls = {}

    def fake_add_to_cart(slug, quantity):
        calls["added"] = (slug, quantity)

    monkeypatch.setattr("app.features.cart.routes.service.add_to_cart", fake_add_to_cart)

    response = client.post("/cart/add", data={"product_slug": "organic-dog-meal", "quantity": "2"})
    assert response.status_code == 302
    location_path = urlparse(response.headers["Location"]).path
    assert location_path == "/cart/"
    assert calls["added"] == ("organic-dog-meal", 2)


def test_update_item_redirects(client, monkeypatch):
    calls = {}

    def fake_update_item(slug, quantity):
        calls["updated"] = (slug, quantity)

    monkeypatch.setattr("app.features.cart.routes.service.update_item", fake_update_item)

    response = client.post("/cart/update", data={"product_slug": "organic-dog-meal", "quantity": "3"})
    assert response.status_code == 302
    location_path = urlparse(response.headers["Location"]).path
    assert location_path == "/cart/"
    assert calls["updated"] == ("organic-dog-meal", 3)


def test_remove_item_redirects(client, monkeypatch):
    calls = {}

    def fake_remove_item(slug):
        calls["removed"] = slug

    monkeypatch.setattr("app.features.cart.routes.service.remove_item", fake_remove_item)

    response = client.post("/cart/remove", data={"product_slug": "organic-dog-meal"})
    assert response.status_code == 302
    location_path = urlparse(response.headers["Location"]).path
    assert location_path == "/cart/"
    assert calls["removed"] == "organic-dog-meal"


def test_checkout_get_renders_form(client, monkeypatch, sample_cart_summary):
    monkeypatch.setattr("app.features.cart.routes.service.get_summary", lambda: sample_cart_summary)

    response = client.get("/cart/checkout")
    assert response.status_code == 200
    assert "結帳資訊" in response.get_data(as_text=True)


def test_checkout_redirects_to_thank_you(client, monkeypatch, sample_cart_summary):
    order_number = "PS250101000000"

    summary_calls = {"count": 0}

    def fake_get_summary():
        summary_calls["count"] += 1
        return sample_cart_summary

    monkeypatch.setattr("app.features.cart.routes.service.get_summary", fake_get_summary)
    monkeypatch.setattr("app.features.cart.routes.service.checkout", lambda form: order_number)

    response = client.post(
        "/cart/checkout",
        data={
            "name": "Test Buyer",
            "email": "buyer@example.com",
            "phone": "0912345678",
            "fulfillment_method": "pickup",
            "notes": "Please call before pickup",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    location = urlparse(response.headers["Location"])
    assert location.path == f"/cart/thank-you/{order_number}"
    assert summary_calls["count"] >= 1


def test_checkout_redirects_when_cart_empty(client, monkeypatch):
    empty_summary = {"items": [], "total_quantity": 0, "total_amount": Decimal("0.00")}
    monkeypatch.setattr("app.features.cart.routes.service.get_summary", lambda: empty_summary)

    response = client.get("/cart/checkout", follow_redirects=False)
    assert response.status_code == 302
    location_path = urlparse(response.headers["Location"]).path
    assert location_path == "/products/"
