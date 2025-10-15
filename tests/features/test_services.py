def test_services_page_renders(client, monkeypatch, sample_services):
    monkeypatch.setattr("app.features.services.routes.get_services", lambda: sample_services)

    response = client.get("/services/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert sample_services[0][1] in body
    assert sample_services[0][2] in body
