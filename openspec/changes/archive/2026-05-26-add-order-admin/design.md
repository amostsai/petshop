## Context
The checkout flow persists orders and order items in MySQL. The ECPay integration adds payment status and transaction fields, but there is no staff-facing view to inspect or act on those orders.

## Goals / Non-Goals
- Goals: provide a simple protected admin UI to list orders, filter by payment status, inspect order details, and cancel unpaid/failed orders.
- Non-Goals: full account system, role-based permissions, ECPay refund/cancel API integration, shipment management, inventory restocking, or customer self-service order lookup.

## Decisions
- Use a separate feature module for admin/order management so storefront cart behavior stays focused.
- Protect routes with simple configured credentials suitable for the demo project. Production-grade user management can be added later as a separate capability.
- Treat cancellation as a local order state in the first version. It will not call ECPay refund or cancellation APIs.
- Reuse existing orders and order_items tables. Add the minimal schema change needed to represent cancellation if `payment_status` remains the source of truth.
- Show payment status labels in Traditional Chinese: `待付款`, `已付款`, `付款失敗`, `已取消`.

## Risks
- Simple credential protection is acceptable for a demo but not sufficient for a production admin area.
- If `add-order-admin` is implemented before `add-ecpay-test-payment` is archived, implementation must account for the active payment schema change.
- Local cancellation may diverge from ECPay state if a late callback arrives after staff marks an order cancelled; callback handling must not silently convert cancelled orders to paid without a clear rule.
