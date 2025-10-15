def test_about_page_renders_content(client, monkeypatch, sample_about):
    monkeypatch.setattr("app.features.about.routes.get_about_info", lambda: sample_about)

    response = client.get("/about/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert sample_about[1] in body
