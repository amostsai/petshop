from app.repositories._utils import fetch_all, fetch_one


def fetch_latest(limit: int):
    query = (
        "SELECT id, title, content, created_at FROM news "
        "ORDER BY created_at DESC LIMIT %s;"
    )
    return fetch_all(query, (limit,), error_message="Failed to load latest news")


def fetch_all_news():
    query = "SELECT id, title, content, created_at FROM news ORDER BY created_at DESC;"
    return fetch_all(query, error_message="Failed to load news list")


def fetch_news_detail(news_id: int):
    query = "SELECT id, title, content, created_at FROM news WHERE id=%s;"
    return fetch_one(query, (news_id,), error_message="Failed to load news detail")
