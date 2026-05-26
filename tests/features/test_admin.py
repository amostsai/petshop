from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse


def _login(client):
    return client.post("/admin/login", data={"username": "admin", "password": "admin"})


def test_admin_orders_redirects_to_login(client):
    response = client.get("/admin/orders", follow_redirects=False)

    assert response.status_code == 302
    location = urlparse(response.headers["Location"])
    assert location.path == "/admin/login"


def test_admin_login_with_configured_credentials(client):
    response = _login(client)

    assert response.status_code == 302
    location = urlparse(response.headers["Location"])
    assert location.path == "/admin/orders"


def test_admin_orders_filters_by_payment_status(client, monkeypatch):
    calls = {}
    orders = [
        {
            "order_number": "PS250101000000",
            "customer_name": "Test Buyer",
            "customer_email": "buyer@example.com",
            "total_amount": Decimal("840.00"),
            "payment_status": "pending",
            "created_at": datetime(2025, 1, 1, 12, 0, 0),
        }
    ]

    def fake_list_orders(payment_status=None):
        calls["payment_status"] = payment_status
        return orders

    monkeypatch.setattr("app.features.admin.routes.service.list_orders", fake_list_orders)
    _login(client)

    response = client.get("/admin/orders?status=pending")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "PS250101000000" in body
    assert "待付款" in body
    assert calls["payment_status"] == "pending"


def test_admin_order_detail_renders_items(client, monkeypatch):
    order = {
        "order_number": "PS250101000000",
        "customer_name": "Test Buyer",
        "customer_email": "buyer@example.com",
        "customer_phone": "0912345678",
        "fulfillment_method": "pickup",
        "notes": "Please call",
        "total_amount": Decimal("840.00"),
        "payment_status": "paid",
        "ecpay_trade_no": "2501011234567890",
        "ecpay_payment_type": "Credit_CreditCard",
        "ecpay_payment_date": datetime(2025, 1, 1, 12, 5, 0),
        "ecpay_return_message": "Succeeded",
        "items": [
            {
                "product_name": "有機鮮肉主食餐 (狗)",
                "unit_price": Decimal("420.00"),
                "quantity": 2,
                "line_total": Decimal("840.00"),
            }
        ],
    }
    monkeypatch.setattr("app.features.admin.routes.service.get_order_detail", lambda order_number: order)
    _login(client)

    response = client.get("/admin/orders/PS250101000000")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "有機鮮肉主食餐 (狗)" in body
    assert "已付款" in body
    assert "2501011234567890" in body


def test_admin_order_detail_missing_returns_404(client, monkeypatch):
    monkeypatch.setattr("app.features.admin.routes.service.get_order_detail", lambda order_number: None)
    _login(client)

    response = client.get("/admin/orders/NOPE")

    assert response.status_code == 404


def test_admin_cancel_order_redirects_to_detail(client, monkeypatch):
    calls = {}

    def fake_cancel_order(order_number):
        calls["order_number"] = order_number
        return True

    monkeypatch.setattr("app.features.admin.routes.service.cancel_order", fake_cancel_order)
    _login(client)

    response = client.post("/admin/orders/PS250101000000/cancel", follow_redirects=False)

    assert response.status_code == 302
    assert calls["order_number"] == "PS250101000000"
    location = urlparse(response.headers["Location"])
    assert location.path == "/admin/orders/PS250101000000"
