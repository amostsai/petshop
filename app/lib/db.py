from contextlib import contextmanager

import mysql.connector
from flask import current_app, g


def init_app(app):
    """Register teardown handlers for connection lifecycle."""
    app.teardown_appcontext(close_db_conn)


def close_db_conn(exception=None):
    conn = g.pop('db_conn', None)
    if conn:
        conn.close()


def get_db_conn():
    """Return a cached connection stored on Flask's g object."""
    conn = g.get('db_conn')
    if conn is None:
        config = current_app.config
        conn = mysql.connector.connect(
            host=config['MYSQL_HOST'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE'],
            port=config['MYSQL_PORT'],
            charset=config.get('MYSQL_CHARSET', 'utf8mb4'),
        )
        g.db_conn = conn
    return conn


@contextmanager
def get_cursor(dictionary=False):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
    finally:
        cursor.close()
