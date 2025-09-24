from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.lib.errors import DataAccessError

from . import bp
from .service import create_contact


@bp.route('', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if name and email and message:
            try:
                create_contact(name, email, message)
            except DataAccessError:
                current_app.logger.exception("Failed to save contact message")
                flash('系統忙線中，請稍後再試一次。', 'danger')
            else:
                flash('感謝您的留言，我們會盡快與您聯絡！', 'success')
            return redirect(url_for('contact.contact'))

        flash('請完整填寫所有欄位', 'danger')
        return redirect(url_for('contact.contact'))

    return render_template('contact.html')
