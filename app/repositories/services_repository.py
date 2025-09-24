from app.repositories._utils import fetch_all


def fetch_services(limit: int | None = None):
    base_query = "SELECT id, name, description, image_url FROM services"
    if limit is not None:
        query = base_query + " LIMIT %s;"
        params = (limit,)
    else:
        query = base_query + ";"
        params = None
    return fetch_all(query, params, error_message="Failed to load services")
