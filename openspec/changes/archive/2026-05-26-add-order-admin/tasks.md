## 1. Implementation
- [x] 1.1 Add admin configuration for credentials/session protection using secret-aware settings.
- [x] 1.2 Extend order payment state to support `cancelled` or add an equivalent cancellation field.
- [x] 1.3 Add repository queries for paginated order lists, payment-status filters, and order details with items.
- [x] 1.4 Add protected admin routes for login/logout, order list, order detail, and cancel action.
- [x] 1.5 Add Jinja templates for dense staff-facing order list, filters, status labels, and detail view.
- [x] 1.6 Ensure ECPay callbacks handle already-cancelled orders according to the chosen rule.
- [x] 1.7 Add focused tests for access protection, status filtering, detail rendering, cancel action, and callback/cancel interaction.
- [x] 1.8 Update README with admin usage and credential configuration.

## 2. Validation
- [x] 2.1 Run `openspec validate add-order-admin --strict`.
- [x] 2.2 Run the relevant admin/cart tests.
- [x] 2.3 Smoke test admin order list/detail/cancel flows in Docker.
