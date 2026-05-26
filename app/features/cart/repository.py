from typing import Any, Iterable

from mysql.connector import Error

from app.lib.db import get_db_conn
from app.lib.errors import DataAccessError


def create_order(order_values: dict[str, Any], order_items: Iterable[dict[str, Any]]) -> int:
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        insert_order_sql = """
            INSERT INTO orders (
                order_number,
                customer_name,
                customer_email,
                customer_phone,
                fulfillment_method,
                notes,
                total_amount,
                payment_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            insert_order_sql,
            (
                order_values['order_number'],
                order_values['customer_name'],
                order_values['customer_email'],
                order_values['customer_phone'],
                order_values['fulfillment_method'],
                order_values.get('notes'),
                order_values['total_amount'],
                order_values.get('payment_status', 'pending'),
            ),
        )
        order_id = cursor.lastrowid

        insert_item_sql = """
            INSERT INTO order_items (
                order_id,
                product_id,
                product_name,
                unit_price,
                quantity,
                line_total
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        item_params = [
            (
                order_id,
                item['product_id'],
                item['product_name'],
                item['unit_price'],
                item['quantity'],
                item['line_total'],
            )
            for item in order_items
        ]
        cursor.executemany(insert_item_sql, item_params)

        conn.commit()
        return order_id
    except Error as exc:
        conn.rollback()
        raise DataAccessError("Failed to create order", original=exc) from exc
    finally:
        cursor.close()


def update_payment_result(order_number: str, payment_values: dict[str, Any]) -> bool:
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        update_sql = """
            UPDATE orders
               SET payment_status = %s,
                   ecpay_trade_no = %s,
                   ecpay_payment_type = %s,
                   ecpay_payment_date = %s,
                   ecpay_return_code = %s,
                   ecpay_return_message = %s
             WHERE order_number = %s;
        """
        cursor.execute(
            update_sql,
            (
                payment_values['payment_status'],
                payment_values.get('ecpay_trade_no'),
                payment_values.get('ecpay_payment_type'),
                payment_values.get('ecpay_payment_date'),
                payment_values.get('ecpay_return_code'),
                payment_values.get('ecpay_return_message'),
                order_number,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as exc:
        conn.rollback()
        raise DataAccessError("Failed to update order payment result", original=exc) from exc
    finally:
        cursor.close()


def fetch_order_payment_status(order_number: str) -> dict[str, Any] | None:
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT order_number, payment_status, ecpay_return_message
              FROM orders
             WHERE order_number = %s;
            """,
            (order_number,),
        )
        return cursor.fetchone()
    except Error as exc:
        raise DataAccessError("Failed to fetch order payment status", original=exc) from exc
    finally:
        cursor.close()
