## Why
After adding online payment, store staff need a way to review which orders are unpaid, paid, or failed/cancelled without querying MySQL manually. A small order admin area will make payment follow-up and customer service practical.

## What Changes
- Add an internal order administration view for listing orders.
- Support filtering by payment status: pending, paid, failed, and cancelled.
- Add an order detail view showing customer info, order items, total amount, payment status, and ECPay transaction fields.
- Allow staff to mark an unpaid or failed order as cancelled inside the app.
- Add basic access protection for the admin routes using configured credentials.

## Impact
- Affected specs: order-admin
- Affected code: new `app/features/admin/` or `app/features/orders/` module, `app/features/cart/repository.py`, `app/config.py`, `app/app.py`, `env/mysql/init.sql`, tests
- Data impact: `orders.payment_status` needs a `cancelled` state or an equivalent cancellation field.
- Related active change: `add-ecpay-test-payment` introduces the payment status fields this admin view will read.
