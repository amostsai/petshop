from flask import render_template
from . import services_bp
from lib.db import get_db_conn

@services_bp.route('/')
def services_list():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, image_url FROM services;")
    services = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('services.html', services=services)
