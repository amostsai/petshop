from flask import current_app

from app.lib.cache import cache
from app.repositories import about_repository


def _ttl() -> int:
    return int(current_app.config.get('CACHE_ABOUT_TTL', current_app.config.get('CACHE_DEFAULT_TTL', 300)))


def get_about_info(*, use_cache: bool = True):
    cache_key = "about:info"
    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    about_info = about_repository.fetch_about_info()
    if about_info:
        cache.set(cache_key, about_info, ttl=_ttl())
    return about_info


def invalidate_cache():
    cache.invalidate("about:")
