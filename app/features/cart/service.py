from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import secrets
from typing import Any, Dict

from app.features.products import repository as product_repository
from app.lib import cart as cart_utils
from app.lib.errors import DataAccessError

from . import repository


class CartError(Exception):
    """Raised when cart operations fail due to validation errors."""


@dataclass
class CheckoutData:
    customer_name: str
    customer_email: str
    customer_phone: str
    fulfillment_method: str
    notes: str | None


def _primary_image(product: Dict[str, Any]) -> str:
    images = product.get('images') or []
    if not images:
        return '/static/images/dog1.png'
    primary = next((img for img in images if img.get('is_primary')), images[0])
    return primary.get('image_url', '/static/images/dog1.png')


def add_to_cart(product_slug: str, quantity: int):
    if quantity <= 0:
        raise CartError("請選擇有效的數量")
    product = product_repository.fetch_product_detail(product_slug)
    if not product:
        raise CartError("找不到該商品，請重新選購")
    if product['stock'] <= 0:
        raise CartError("此商品目前缺貨")

    cart_utils.add_product(product, quantity, image_url=_primary_image(product))
    return cart_utils.summarize()


def update_item(product_slug: str, quantity: int):
    if quantity <= 0:
        cart_utils.remove_item(product_slug)
        return cart_utils.summarize()

    product = product_repository.fetch_product_detail(product_slug)
    if not product or product['stock'] <= 0:
        cart_utils.remove_item(product_slug)
        raise CartError("商品已下架或缺貨，已從購物車移除")

    cart_utils.update_quantity(product_slug, quantity, stock=int(product['stock']))
    return cart_utils.summarize()


def remove_item(product_slug: str):
    cart_utils.remove_item(product_slug)
    return cart_utils.summarize()


def get_summary():
    return cart_utils.summarize()


def _generate_order_number() -> str:
    timestamp = datetime.now().strftime("PS%y%m%d%H%M%S")
    suffix = secrets.token_hex(2).upper()
    return f"{timestamp}{suffix}"[:20]


def _validate_checkout_form(form_data: Dict[str, Any]) -> CheckoutData:
    name = (form_data.get('name') or '').strip()
    email = (form_data.get('email') or '').strip()
    phone = (form_data.get('phone') or '').strip()
    fulfillment_method = form_data.get('fulfillment_method', '').strip()
    notes = (form_data.get('notes') or '').strip() or None

    if not name:
        raise CartError("請輸入聯絡人姓名")
    if not email:
        raise CartError("請輸入電子郵件")
    if '@' not in email:
        raise CartError("請輸入有效的電子郵件格式")
    if not phone:
        raise CartError("請輸入聯絡電話")
    if fulfillment_method not in {'pickup', 'delivery'}:
        raise CartError("請選擇取貨方式")

    return CheckoutData(
        customer_name=name,
        customer_email=email,
        customer_phone=phone,
        fulfillment_method=fulfillment_method,
        notes=notes,
    )


def checkout(form_data: Dict[str, Any]) -> str:
    summary = cart_utils.summarize()
    if summary['total_quantity'] == 0:
        raise CartError("購物車為空，請先選購商品")

    checkout_data = _validate_checkout_form(form_data)

    validated_items = []
    total_amount = Decimal('0.00')

    for item in summary['items']:
        product = product_repository.fetch_product_detail(item['product_slug'])
        if not product or product['stock'] <= 0:
            cart_utils.remove_item(item['product_slug'])
            raise CartError(f"{item['name']} 已停售或缺貨，請重新確認購物車")

        desired_qty = int(item['quantity'])
        available_stock = int(product['stock'])
        if desired_qty > available_stock:
            cart_utils.update_quantity(item['product_slug'], available_stock, stock=available_stock)
            raise CartError(f"{item['name']} 庫存不足，已調整為{available_stock}件")

        unit_price = Decimal(str(product['price'])).quantize(Decimal('0.01'))
        line_total = (unit_price * desired_qty).quantize(Decimal('0.01'))
        total_amount += line_total

        validated_items.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'unit_price': unit_price,
            'quantity': desired_qty,
            'line_total': line_total,
        })

    order_number = _generate_order_number()
    order_payload = {
        'order_number': order_number,
        'customer_name': checkout_data.customer_name,
        'customer_email': checkout_data.customer_email,
        'customer_phone': checkout_data.customer_phone,
        'fulfillment_method': checkout_data.fulfillment_method,
        'notes': checkout_data.notes,
        'total_amount': total_amount.quantize(Decimal('0.01')),
    }

    repository.create_order(order_payload, validated_items)
    cart_utils.clear_cart()
    return order_number
