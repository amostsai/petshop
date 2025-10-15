from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.lib.errors import DataAccessError

from . import bp
from . import service
from .service import CartError


@bp.route('/')
def view_cart():
    summary = service.get_summary()
    return render_template('cart.html', summary=summary)


@bp.route('/add', methods=['POST'])
def add_item():
    product_slug = request.form.get('product_slug', '').strip()
    if not product_slug:
        abort(400)
    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    try:
        service.add_to_cart(product_slug, quantity)
        flash("已將商品加入購物車！", 'success')
    except CartError as exc:
        flash(str(exc), 'error')
    except DataAccessError:
        current_app.logger.exception("Failed to add product to cart", extra={'slug': product_slug})
        flash("加入購物車時發生錯誤，請稍後再試", 'error')

    return redirect(url_for('cart.view_cart'))


@bp.route('/update', methods=['POST'])
def update_item():
    product_slug = request.form.get('product_slug', '').strip()
    if not product_slug:
        abort(400)
    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    try:
        service.update_item(product_slug, quantity)
        flash("已更新購物車", 'success')
    except CartError as exc:
        flash(str(exc), 'error')
    except DataAccessError:
        current_app.logger.exception("Failed to update cart item", extra={'slug': product_slug})
        flash("更新購物車時發生錯誤，請稍後再試", 'error')

    return redirect(url_for('cart.view_cart'))


@bp.route('/remove', methods=['POST'])
def remove_item():
    product_slug = request.form.get('product_slug', '').strip()
    if not product_slug:
        abort(400)
    try:
        service.remove_item(product_slug)
        flash("已從購物車移除商品", 'success')
    except DataAccessError:
        current_app.logger.exception("Failed to remove cart item", extra={'slug': product_slug})
        flash("移除商品時發生錯誤，請稍後再試", 'error')
    return redirect(url_for('cart.view_cart'))


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    summary = service.get_summary()
    if summary['total_quantity'] == 0:
        flash("購物車為空，請先選購商品", 'error')
        return redirect(url_for('products.catalog'))

    if request.method == 'POST':
        try:
            order_number = service.checkout(request.form)
            return redirect(url_for('cart.thank_you', order_number=order_number))
        except CartError as exc:
            flash(str(exc), 'error')
        except DataAccessError:
            current_app.logger.exception("Failed to checkout order")
            flash("結帳時發生錯誤，請稍後再試", 'error')
        return redirect(url_for('cart.checkout'))

    return render_template('checkout.html', summary=summary)


@bp.route('/thank-you/<order_number>')
def thank_you(order_number: str):
    if not order_number:
        abort(404)
    return render_template('thank_you.html', order_number=order_number)
