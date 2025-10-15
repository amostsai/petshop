import os
from datetime import datetime
from decimal import Decimal

import pytest

from app import create_app


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("APP_ENV", "testing")
    application = create_app("testing")
    application.config.update(TESTING=True)
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def sample_news_items():
    now = datetime(2025, 1, 1, 10, 0, 0)
    return [
        (1, "夏日寵物健檢優惠", "即日起至8月底，帶您的毛孩來店享受健檢8折優惠！", now),
        (2, "寵物美容新服務上線", "全新SPA寵物美容，給毛孩最頂級的呵護，歡迎預約！", now),
    ]


@pytest.fixture()
def sample_services():
    return [
        (1, "寵物美容", "專業美容師團隊，提供洗澡、剪毛、SPA等多元服務。", "/static/images/services/grooming.png"),
        (2, "寵物寄宿", "舒適安全的寄宿空間，24小時照護，讓您安心出遊。", "/static/images/services/boarding.png"),
    ]


@pytest.fixture()
def sample_about():
    return (1, "我們是一群熱愛動物的專業團隊。", "/static/images/about/team.webp")


@pytest.fixture()
def sample_products():
    return [
        {
            "id": 1,
            "name": "有機鮮肉主食餐 (狗)",
            "slug": "organic-dog-meal",
            "description": "採用人食等級鮮肉與蔬菜製成。",
            "price": Decimal("420.00"),
            "stock": 25,
            "category_name": "寵物主食",
            "category_slug": "pet-food",
            "image_url": "/static/images/products/dog-meal.png",
            "images": [{"image_url": "/static/images/products/dog-meal.png", "is_primary": 1}],
        },
        {
            "id": 2,
            "name": "逗貓智能球",
            "slug": "smart-cat-ball",
            "description": "互動逗貓球，自動感測變速。",
            "price": Decimal("680.00"),
            "stock": 18,
            "category_name": "玩具配件",
            "category_slug": "toys-accessories",
            "image_url": "/static/images/products/cat-ball.png",
            "images": [{"image_url": "/static/images/products/cat-ball.png", "is_primary": 1}],
        },
    ]


@pytest.fixture()
def sample_cart_summary(sample_products):
    first_item = sample_products[0]
    return {
        "items": [
            {
                "product_id": first_item["id"],
                "product_slug": first_item["slug"],
                "name": first_item["name"],
                "unit_price": str(first_item["price"]),
                "unit_price_amount": Decimal(str(first_item["price"])),
                "quantity": 2,
                "stock": first_item["stock"],
                "image_url": first_item["image_url"],
                "line_total": Decimal("840.00"),
            }
        ],
        "total_quantity": 2,
        "total_amount": Decimal("840.00"),
    }
