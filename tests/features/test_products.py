import copy


def test_product_catalog_lists_items(client, monkeypatch, sample_products):
    categories = [
        {"id": 1, "name": "寵物主食", "slug": "pet-food", "description": "主食"},
        {"id": 2, "name": "玩具配件", "slug": "toys-accessories", "description": "玩具"},
    ]
    captured_category = {}

    def fake_get_categories():
        return categories

    def fake_get_catalog(category_slug=None):
        captured_category["value"] = category_slug
        if category_slug == "pet-food":
            return [sample_products[0]]
        if category_slug == "toys-accessories":
            return [sample_products[1]]
        return sample_products

    monkeypatch.setattr("app.features.products.routes.service.get_categories", fake_get_categories)
    monkeypatch.setattr("app.features.products.routes.service.get_catalog", fake_get_catalog)

    response = client.get("/products/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert sample_products[0]["name"] in body
    assert sample_products[1]["name"] in body

    filtered = client.get("/products/?category=pet-food")
    assert filtered.status_code == 200
    assert captured_category["value"] == "pet-food"
    assert sample_products[0]["name"] in filtered.get_data(as_text=True)
    assert sample_products[1]["name"] not in filtered.get_data(as_text=True)


def test_product_detail_page(client, monkeypatch, sample_products):
    product_detail = copy.deepcopy(sample_products[0])

    def fake_get_product_detail(slug):
        if slug == product_detail["slug"]:
            return product_detail
        return None

    monkeypatch.setattr("app.features.products.routes.service.get_product_detail", fake_get_product_detail)

    response = client.get(f"/products/{product_detail['slug']}")
    assert response.status_code == 200
    assert product_detail["name"] in response.get_data(as_text=True)
