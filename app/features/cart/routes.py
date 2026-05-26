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
from .ecpay import build_checkout_params, generate_check_mac_value
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
            order = service.checkout(request.form)
            return_url = current_app.config.get('ECPAY_RETURN_URL') or url_for('cart.ecpay_return', _external=True)
            client_back_url = current_app.config.get('ECPAY_CLIENT_BACK_URL') or url_for(
                'cart.thank_you',
                order_number=order.order_number,
                _external=True,
            )
            ecpay_params = build_checkout_params(
                merchant_id=current_app.config['ECPAY_MERCHANT_ID'],
                order_number=order.order_number,
                total_amount=order.total_amount,
                item_names=order.item_names,
                return_url=return_url,
                client_back_url=client_back_url,
            )
            ecpay_params['CheckMacValue'] = generate_check_mac_value(
                ecpay_params,
                hash_key=current_app.config['ECPAY_HASH_KEY'],
                hash_iv=current_app.config['ECPAY_HASH_IV'],
            )
            return render_template(
                'ecpay_redirect.html',
                checkout_url=current_app.config['ECPAY_CHECKOUT_URL'],
                ecpay_params=ecpay_params,
                order_number=order.order_number,
            )
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
    payment_status = None
    try:
        payment_status = service.get_order_payment_status(order_number)
    except DataAccessError:
        current_app.logger.exception("Failed to load order payment status")
    return render_template('thank_you.html', order_number=order_number, payment_status=payment_status)


@bp.route('/ecpay/return', methods=['POST'])
def ecpay_return():
    form_data = request.form.to_dict()
    received_order_number = form_data.get('MerchantTradeNo')
    from .ecpay import verify_check_mac_value

    if not verify_check_mac_value(
        form_data,
        hash_key=current_app.config['ECPAY_HASH_KEY'],
        hash_iv=current_app.config['ECPAY_HASH_IV'],
    ):
        current_app.logger.warning("Rejected ECPay callback with invalid CheckMacValue")
        return '0|CheckMacValue Error', 400

    try:
        updated = service.record_ecpay_result(form_data)
    except (CartError, DataAccessError):
        current_app.logger.exception("Failed to record ECPay payment result")
        return '0|Error', 500

    if not updated:
        current_app.logger.warning("ECPay callback referenced unknown order", extra={'order_number': received_order_number})
        return '0|Order Not Found', 404

    return '1|OK'
