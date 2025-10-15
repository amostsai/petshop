from flask import abort, current_app, render_template, request

from app.lib.errors import DataAccessError

from . import bp
from . import service


@bp.route('/')
def catalog():
    category_slug = request.args.get('category')
    try:
        categories = service.get_categories()
    except DataAccessError:
        current_app.logger.exception("Failed to load product categories")
        abort(500)

    valid_category_slugs = {c['slug'] for c in categories}
    if category_slug and category_slug not in valid_category_slugs:
        abort(404)

    try:
        products = service.get_catalog(category_slug)
    except DataAccessError:
        current_app.logger.exception("Failed to load product catalog")
        abort(500)

    return render_template(
        'catalog.html',
        categories=categories,
        products=products,
        active_category=category_slug,
    )


@bp.route('/<slug>')
def product_detail(slug: str):
    try:
        product = service.get_product_detail(slug)
    except DataAccessError:
        current_app.logger.exception("Failed to load product detail", extra={'slug': slug})
        abort(500)
    if not product:
        abort(404)

    images = product.get('images', [])
    primary_image = next((img['image_url'] for img in images if img.get('is_primary')), images[0]['image_url'] if images else '/static/images/dog1.png')
    in_stock = product['stock'] > 0

    return render_template(
        'product_detail.html',
        product=product,
        images=images,
        primary_image=primary_image,
        in_stock=in_stock,
    )
