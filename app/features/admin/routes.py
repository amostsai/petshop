from __future__ import annotations

from functools import wraps
from hmac import compare_digest
from typing import Callable

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.lib.errors import DataAccessError

from . import bp
from . import service
from .service import AdminOrderError

ADMIN_SESSION_KEY = 'admin_authenticated'


def _is_authenticated() -> bool:
    return bool(session.get(ADMIN_SESSION_KEY))


def _admin_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not _is_authenticated():
            return redirect(url_for('admin.login', next=request.path))
        return view(*args, **kwargs)

    return wrapped


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''
        expected_username = current_app.config.get('ADMIN_USERNAME') or ''
        expected_password = current_app.config.get('ADMIN_PASSWORD') or ''

        if compare_digest(username, expected_username) and compare_digest(password, expected_password):
            session[ADMIN_SESSION_KEY] = True
            flash("已登入後台", 'success')
            return redirect(request.args.get('next') or url_for('admin.orders'))

        flash("後台帳號或密碼錯誤", 'error')

    return render_template('admin_login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    session.pop(ADMIN_SESSION_KEY, None)
    flash("已登出後台", 'success')
    return redirect(url_for('admin.login'))


@bp.route('/orders')
@_admin_required
def orders():
    payment_status = request.args.get('status')
    try:
        orders_list = service.list_orders(payment_status)
    except DataAccessError:
        current_app.logger.exception("Failed to load admin orders")
        abort(500)

    return render_template(
        'admin_orders.html',
        orders=orders_list,
        selected_status=payment_status,
        status_labels=service.STATUS_LABELS,
    )


@bp.route('/orders/<order_number>')
@_admin_required
def order_detail(order_number: str):
    try:
        order = service.get_order_detail(order_number)
    except DataAccessError:
        current_app.logger.exception("Failed to load admin order detail")
        abort(500)

    if not order:
        abort(404)

    return render_template('admin_order_detail.html', order=order, status_labels=service.STATUS_LABELS)


@bp.route('/orders/<order_number>/cancel', methods=['POST'])
@_admin_required
def cancel_order(order_number: str):
    try:
        cancelled = service.cancel_order(order_number)
    except AdminOrderError as exc:
        flash(str(exc), 'error')
    except DataAccessError:
        current_app.logger.exception("Failed to cancel admin order")
        flash("取消訂單時發生錯誤，請稍後再試", 'error')
    else:
        if cancelled:
            flash("已取消訂單", 'success')
        else:
            flash("訂單狀態未變更", 'error')

    return redirect(url_for('admin.order_detail', order_number=order_number))
