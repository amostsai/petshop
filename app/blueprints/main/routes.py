from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from . import main_bp
from app.lib.errors import DataAccessError
from app.services import contact_service, news_service, services_service


@main_bp.route('/')
def index():
    try:
        news = news_service.get_latest_news(limit=3)
        services = services_service.get_services(limit=4)
    except DataAccessError:
        current_app.logger.exception("Failed to load homepage data")
        abort(500)
    return render_template('index.html', news=news, services=services)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if name and email and message:
            try:
                contact_service.create_contact(name, email, message)
            except DataAccessError:
                current_app.logger.exception("Failed to save contact message")
                flash('系統忙線中，請稍後再試一次。', 'danger')
            else:
                flash('感謝您的留言，我們會盡快與您聯絡！', 'success')
            return redirect(url_for('main.contact'))

        flash('請完整填寫所有欄位', 'danger')
        return redirect(url_for('main.contact'))

    return render_template('contact.html')
