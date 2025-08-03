from flask import render_template
from . import about_bp
from lib.db import get_db_conn

@about_bp.route('/')
def about():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, content, image_url FROM about LIMIT 1;")
    about_info = cur.fetchone()
    cur.close()
    conn.close()
    # 社群連結可直接寫死於模板
    return render_template('about.html', about_info=about_info)
