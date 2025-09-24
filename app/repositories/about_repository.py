from app.repositories._utils import fetch_one


def fetch_about_info():
    query = "SELECT id, content, image_url FROM about LIMIT 1;"
    return fetch_one(query, error_message="Failed to load about information")
