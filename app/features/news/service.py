from flask import current_app

from app.lib.cache import cache

from . import repository


def _ttl() -> int:
    return int(current_app.config.get('CACHE_NEWS_TTL', current_app.config.get('CACHE_DEFAULT_TTL', 60)))


def get_latest_news(limit: int = 3, *, use_cache: bool = True):
    cache_key = f"news:latest:{limit}"
    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    news_items = repository.fetch_latest(limit)
    cache.set(cache_key, news_items, ttl=_ttl())
    return news_items


def get_news_list(*, use_cache: bool = True):
    cache_key = "news:list"
    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    news_items = repository.fetch_all_news()
    cache.set(cache_key, news_items, ttl=_ttl())
    return news_items


def get_news_detail(news_id: int):
    cache_key = f"news:detail:{news_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    news_item = repository.fetch_news_detail(news_id)
    if news_item:
        cache.set(cache_key, news_item, ttl=_ttl())
    return news_item


def invalidate_cache():
    cache.invalidate("news:")
