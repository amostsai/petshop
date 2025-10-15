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
                total_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
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
