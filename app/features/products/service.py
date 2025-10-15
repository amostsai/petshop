from typing import Optional

from app.lib.errors import DataAccessError

from . import repository


def get_categories():
    return repository.fetch_categories()


def get_catalog(category_slug: Optional[str] = None):
    return repository.fetch_catalog(category_slug)


def get_product_detail(slug: str):
    return repository.fetch_product_detail(slug)
