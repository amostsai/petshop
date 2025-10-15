def test_contact_get_renders_form(client):
    response = client.get("/contact/")
    assert response.status_code == 200
    assert "聯絡我們" in response.get_data(as_text=True)


def test_contact_post_persists_message(client, monkeypatch):
    created_messages = []

    def fake_create_contact(name, email, message):
        created_messages.append((name, email, message))

    monkeypatch.setattr("app.features.contact.routes.create_contact", fake_create_contact)

    response = client.post(
        "/contact/",
        data={
            "name": "Test User",
            "email": "user@example.com",
            "message": "Hello from tests",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact/")
    assert created_messages == [("Test User", "user@example.com", "Hello from tests")]
