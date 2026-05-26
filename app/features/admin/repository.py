from __future__ import annotations

from typing import Any

from mysql.connector import Error

from app.lib.db import get_db_conn
from app.lib.errors import DataAccessError


VALID_PAYMENT_STATUSES = {'pending', 'paid', 'failed', 'cancelled'}


def fetch_orders(payment_status: str | None = None) -> list[dict[str, Any]]:
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        params: tuple[Any, ...] = ()
        where_clause = ''
        if payment_status in VALID_PAYMENT_STATUSES:
            where_clause = 'WHERE payment_status = %s'
            params = (payment_status,)

        cursor.execute(
            f"""
            SELECT order_number,
                   customer_name,
                   customer_email,
                   total_amount,
                   payment_status,
                   created_at
              FROM orders
              {where_clause}
             ORDER BY created_at DESC, id DESC
             LIMIT 100;
            """,
            params,
        )
        return cursor.fetchall()
    except Error as exc:
        raise DataAccessError("Failed to fetch admin orders", original=exc) from exc
    finally:
        cursor.close()


def fetch_order_detail(order_number: str) -> dict[str, Any] | None:
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id,
                   order_number,
                   customer_name,
                   customer_email,
                   customer_phone,
                   fulfillment_method,
                   notes,
                   total_amount,
                   payment_status,
                   ecpay_trade_no,
                   ecpay_payment_type,
                   ecpay_payment_date,
                   ecpay_return_code,
                   ecpay_return_message,
                   created_at
              FROM orders
             WHERE order_number = %s;
            """,
            (order_number,),
        )
        order = cursor.fetchone()
        if not order:
            return None

        cursor.execute(
            """
            SELECT product_name, unit_price, quantity, line_total
              FROM order_items
             WHERE order_id = %s
             ORDER BY id;
            """,
            (order['id'],),
        )
        order['items'] = cursor.fetchall()
        return order
    except Error as exc:
        raise DataAccessError("Failed to fetch admin order detail", original=exc) from exc
    finally:
        cursor.close()


def mark_order_cancelled(order_number: str) -> bool:
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE orders
               SET payment_status = 'cancelled'
             WHERE order_number = %s
               AND payment_status IN ('pending', 'failed');
            """,
            (order_number,),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as exc:
        conn.rollback()
        raise DataAccessError("Failed to cancel order", original=exc) from exc
    finally:
        cursor.close()
