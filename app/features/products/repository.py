from typing import Any, Optional

from mysql.connector import Error

from app.lib.db import get_cursor
from app.lib.errors import DataAccessError


def fetch_categories() -> list[dict[str, Any]]:
    query = "SELECT id, name, slug, COALESCE(description, '') AS description FROM product_categories ORDER BY name;"
    try:
        with get_cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return list(cursor.fetchall())
    except Error as exc:
        raise DataAccessError("Failed to load product categories", original=exc) from exc


def fetch_catalog(category_slug: Optional[str] = None) -> list[dict[str, Any]]:
    params: tuple[Any, ...] = ()
    where_clause = "WHERE p.is_published = 1"
    if category_slug:
        where_clause += " AND c.slug = %s"
        params = (category_slug,)

    query = f"""
        SELECT
            p.id,
            p.name,
            p.slug,
            p.price,
            p.stock,
            c.name AS category_name,
            c.slug AS category_slug,
            COALESCE((
                SELECT image_url
                FROM product_images
                WHERE product_id = p.id
                ORDER BY is_primary DESC, sort_order ASC, id ASC
                LIMIT 1
            ), '/static/images/dog1.png') AS image_url
        FROM products p
        INNER JOIN product_categories c ON p.category_id = c.id
        {where_clause}
        ORDER BY c.name, p.name;
    """
    try:
        with get_cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return list(cursor.fetchall())
    except Error as exc:
        raise DataAccessError("Failed to load product catalog", original=exc) from exc


def fetch_product_detail(slug: str) -> Optional[dict[str, Any]]:
    product_query = """
        SELECT
            p.id,
            p.name,
            p.slug,
            p.description,
            p.price,
            p.stock,
            c.name AS category_name,
            c.slug AS category_slug
        FROM products p
        INNER JOIN product_categories c ON p.category_id = c.id
        WHERE p.slug = %s AND p.is_published = 1;
    """
    try:
        with get_cursor(dictionary=True) as cursor:
            cursor.execute(product_query, (slug,))
            product = cursor.fetchone()
            if not product:
                return None
            image_query = """
                SELECT image_url, is_primary
                FROM product_images
                WHERE product_id = %s
                ORDER BY is_primary DESC, sort_order ASC, id ASC;
            """
            cursor.execute(image_query, (product['id'],))
            images = cursor.fetchall()
    except Error as exc:
        raise DataAccessError("Failed to load product detail", original=exc) from exc

    product['images'] = images or [{'image_url': '/static/images/dog1.png', 'is_primary': 1}]
    return product
