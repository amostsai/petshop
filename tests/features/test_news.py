def test_news_list_and_detail(client, monkeypatch, sample_news_items):
    monkeypatch.setattr("app.features.news.routes.get_news_list", lambda: sample_news_items)

    def fake_get_news_detail(news_id: int):
        for item in sample_news_items:
            if item[0] == news_id:
                return item
        return None

    monkeypatch.setattr("app.features.news.routes.get_news_detail", fake_get_news_detail)

    list_response = client.get("/news/")
    assert list_response.status_code == 200
    assert sample_news_items[0][1] in list_response.get_data(as_text=True)

    detail_response = client.get(f"/news/{sample_news_items[0][0]}")
    assert detail_response.status_code == 200
    assert sample_news_items[0][2] in detail_response.get_data(as_text=True)

    missing_response = client.get("/news/99999")
    assert missing_response.status_code == 404
