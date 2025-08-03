from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from lib.db import get_db_conn

# 首頁路由
@main_bp.route('/')
def index():
    # 查詢 3 則最新消息、4 項服務，傳給首頁模板
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, created_at FROM news ORDER BY created_at DESC LIMIT 3;")
    news = cur.fetchall()
    cur.execute("SELECT id, name, description, image_url FROM services LIMIT 4;")
    services = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', news=news, services=services)

# 聯絡表單路由
@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 從表單取得資料
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        # 後端驗證
        if name and email and message:
            # 寫入 contact table
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('感謝您的留言，我們會盡快與您聯絡！', 'success')
        else:
            flash('請完整填寫所有欄位', 'danger')
        return redirect(url_for('main.contact'))
    # GET 請求直接渲染表單
    return render_template('contact.html')
