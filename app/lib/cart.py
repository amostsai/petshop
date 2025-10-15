from __future__ import annotations

from decimal import Decimal
from typing import Any

from flask import session

CART_SESSION_KEY = 'cart'


def _ensure_cart() -> dict[str, Any]:
    cart = session.get(CART_SESSION_KEY)
    if not cart or 'items' not in cart:
        cart = {'items': []}
        session[CART_SESSION_KEY] = cart
        session.modified = True
    return cart


def get_cart() -> dict[str, Any]:
    return _ensure_cart()


def clear_cart() -> None:
    if CART_SESSION_KEY in session:
        session.pop(CART_SESSION_KEY, None)
        session.modified = True


def add_product(product: dict[str, Any], quantity: int, *, image_url: str) -> None:
    if quantity <= 0:
        return
    stock = int(product.get('stock', 0) or 0)
    if stock <= 0:
        return

    cart = _ensure_cart()
    items = cart['items']
    for item in items:
        if item['product_slug'] == product['slug']:
            item['quantity'] = min(item['quantity'] + quantity, stock)
            item['stock'] = stock
            item['unit_price'] = str(product['price'])
            item['image_url'] = image_url
            session.modified = True
            return

    items.append({
        'product_id': int(product['id']),
        'product_slug': product['slug'],
        'name': product['name'],
        'unit_price': str(product['price']),
        'quantity': min(quantity, stock),
        'image_url': image_url,
        'stock': stock,
    })
    session.modified = True


def update_quantity(slug: str, quantity: int, *, stock: int | None = None) -> None:
    cart = _ensure_cart()
    items = cart['items']
    for item in list(items):
        if item['product_slug'] != slug:
            continue
        if quantity <= 0:
            items.remove(item)
        else:
            max_stock = stock if stock is not None else item.get('stock', quantity)
            item['quantity'] = min(quantity, max_stock if max_stock is not None else quantity)
            if stock is not None:
                item['stock'] = stock
        session.modified = True
        return


def remove_item(slug: str) -> None:
    cart = _ensure_cart()
    items = cart['items']
    filtered = [item for item in items if item['product_slug'] != slug]
    if len(filtered) != len(items):
        cart['items'] = filtered
        session[CART_SESSION_KEY] = cart
        session.modified = True


def summarize() -> dict[str, Any]:
    cart = session.get(CART_SESSION_KEY) or {'items': []}
    total_quantity = 0
    total_amount = Decimal('0.00')
    summarized_items: list[dict[str, Any]] = []
    for item in cart.get('items', []):
        quantity = int(item['quantity'])
        unit_price = Decimal(str(item['unit_price']))
        line_total = (unit_price * quantity).quantize(Decimal('0.01'))
        total_quantity += quantity
        total_amount += line_total
        summarized_item = dict(item)
        summarized_item['unit_price_amount'] = unit_price
        summarized_item['line_total'] = line_total
        summarized_items.append(summarized_item)
    return {
        'items': summarized_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount.quantize(Decimal('0.01')),
    }
