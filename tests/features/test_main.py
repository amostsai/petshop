def test_homepage_renders_news_and_services(client, monkeypatch, sample_news_items, sample_services):
    def fake_get_latest_news(limit=3, use_cache=True):
        return sample_news_items[:limit]

    def fake_get_services(limit=None, use_cache=True):
        return sample_services if limit is None else sample_services[:limit]

    monkeypatch.setattr("app.features.news.service.get_latest_news", fake_get_latest_news)
    monkeypatch.setattr("app.features.services.service.get_services", fake_get_services)

    response = client.get("/")
    assert response.status_code == 200
    assert sample_news_items[0][1] in response.get_data(as_text=True)
    assert sample_services[0][1] in response.get_data(as_text=True)
