from decimal import Decimal
from urllib.parse import urlparse

from app.features.cart.ecpay import generate_check_mac_value
from app.features.cart.service import CheckoutOrder


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


def test_checkout_renders_ecpay_redirect_form(client, monkeypatch, sample_cart_summary):
    order_number = "PS250101000000"

    summary_calls = {"count": 0}

    def fake_get_summary():
        summary_calls["count"] += 1
        return sample_cart_summary

    monkeypatch.setattr("app.features.cart.routes.service.get_summary", fake_get_summary)
    monkeypatch.setattr(
        "app.features.cart.routes.service.checkout",
        lambda form: CheckoutOrder(
            order_number=order_number,
            total_amount=Decimal("840.00"),
            item_names=["有機鮮肉主食餐 (狗)"],
        ),
    )

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

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5" in body
    assert f'name="MerchantTradeNo" value="{order_number}"' in body
    assert 'name="CheckMacValue"' in body
    assert summary_calls["count"] >= 1


def test_checkout_redirects_when_cart_empty(client, monkeypatch):
    empty_summary = {"items": [], "total_quantity": 0, "total_amount": Decimal("0.00")}
    monkeypatch.setattr("app.features.cart.routes.service.get_summary", lambda: empty_summary)

    response = client.get("/cart/checkout", follow_redirects=False)
    assert response.status_code == 302
    location_path = urlparse(response.headers["Location"]).path
    assert location_path == "/products/"


def test_ecpay_return_updates_verified_payment(client, monkeypatch, app):
    calls = {}
    form_data = {
        "MerchantID": app.config["ECPAY_MERCHANT_ID"],
        "MerchantTradeNo": "PS250101000000",
        "RtnCode": "1",
        "RtnMsg": "Succeeded",
        "TradeNo": "2501011234567890",
        "PaymentType": "Credit_CreditCard",
        "PaymentDate": "2025/01/01 12:00:00",
    }
    form_data["CheckMacValue"] = generate_check_mac_value(
        form_data,
        hash_key=app.config["ECPAY_HASH_KEY"],
        hash_iv=app.config["ECPAY_HASH_IV"],
    )

    def fake_record_ecpay_result(data):
        calls["data"] = data
        return True

    monkeypatch.setattr("app.features.cart.routes.service.record_ecpay_result", fake_record_ecpay_result)

    response = client.post("/cart/ecpay/return", data=form_data)

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "1|OK"
    assert calls["data"]["MerchantTradeNo"] == "PS250101000000"


def test_ecpay_return_rejects_invalid_check_mac_value(client, monkeypatch):
    calls = {"recorded": False}

    def fake_record_ecpay_result(data):
        calls["recorded"] = True
        return True

    monkeypatch.setattr("app.features.cart.routes.service.record_ecpay_result", fake_record_ecpay_result)

    response = client.post(
        "/cart/ecpay/return",
        data={
            "MerchantID": "3002607",
            "MerchantTradeNo": "PS250101000000",
            "RtnCode": "1",
            "CheckMacValue": "INVALID",
        },
    )

    assert response.status_code == 400
    assert response.get_data(as_text=True) == "0|CheckMacValue Error"
    assert calls["recorded"] is False
