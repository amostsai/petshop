from flask import render_template, abort
from . import news_bp
from lib.db import get_db_conn

@news_bp.route('/')
def news_list():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, created_at FROM news ORDER BY created_at DESC;")
    news = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('news.html', news=news)

@news_bp.route('/<int:news_id>')
def news_detail(news_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, created_at FROM news WHERE id=%s;", (news_id,))
    news = cur.fetchone()
    cur.close()
    conn.close()
    if not news:
        abort(404)
    return render_template('news_detail.html', news=news)
