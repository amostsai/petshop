from flask import current_app

from app.lib.cache import cache
from app.repositories import services_repository


def _ttl() -> int:
    return int(current_app.config.get('CACHE_SERVICES_TTL', current_app.config.get('CACHE_DEFAULT_TTL', 60)))


def get_services(limit: int | None = None, *, use_cache: bool = True):
    cache_key = f"services:{limit if limit is not None else 'all'}"
    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
    services = services_repository.fetch_services(limit)
    cache.set(cache_key, services, ttl=_ttl())
    return services


def invalidate_cache():
    cache.invalidate("services:")
