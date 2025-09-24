from typing import Any, Iterable

from mysql.connector import Error

from app.lib.db import get_db_conn, get_cursor
from app.lib.errors import DataAccessError


def fetch_all(query: str, params: Iterable[Any] | None = None, *, error_message: str):
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    except Error as exc:
        raise DataAccessError(error_message, original=exc) from exc


def fetch_one(query: str, params: Iterable[Any] | None = None, *, error_message: str):
    try:
        with get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    except Error as exc:
        raise DataAccessError(error_message, original=exc) from exc


def execute(query: str, params: Iterable[Any] | None = None, *, error_message: str, commit: bool = False):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
    except Error as exc:
        if commit:
            conn.rollback()
        raise DataAccessError(error_message, original=exc) from exc
    finally:
        cursor.close()
