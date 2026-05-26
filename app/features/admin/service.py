from __future__ import annotations

from typing import Any

from . import repository

STATUS_LABELS = {
    'pending': '待付款',
    'paid': '已付款',
    'failed': '付款失敗',
    'cancelled': '已取消',
}


class AdminOrderError(Exception):
    """Raised when an admin order action cannot be completed."""


def list_orders(payment_status: str | None = None) -> list[dict[str, Any]]:
    selected_status = payment_status if payment_status in repository.VALID_PAYMENT_STATUSES else None
    return repository.fetch_orders(selected_status)


def get_order_detail(order_number: str) -> dict[str, Any] | None:
    return repository.fetch_order_detail(order_number)


def cancel_order(order_number: str) -> bool:
    order = repository.fetch_order_detail(order_number)
    if not order:
        raise AdminOrderError("找不到訂單")
    if order['payment_status'] == 'paid':
        raise AdminOrderError("已付款訂單不能在後台直接取消")
    if order['payment_status'] == 'cancelled':
        return True
    return repository.mark_order_cancelled(order_number)
