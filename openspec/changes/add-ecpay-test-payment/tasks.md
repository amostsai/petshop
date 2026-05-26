## 1. Implementation
- [x] 1.1 Add ECPay configuration values and stage defaults.
- [x] 1.2 Extend the orders schema with payment status and ECPay transaction fields.
- [x] 1.3 Add repository helpers to update payment state by order number.
- [x] 1.4 Add an ECPay helper for checkout parameters and CheckMacValue generation/verification.
- [x] 1.5 Update checkout POST to create an order and render an auto-submit ECPay redirect form.
- [x] 1.6 Add ECPay return callback route that verifies CheckMacValue and updates order payment status.
- [x] 1.7 Update thank-you/payment result views and messages for pending/paid/failed states.
- [x] 1.8 Add focused tests for parameter generation, checkout redirect, callback verification, and failed callbacks.

## 2. Validation
- [x] 2.1 Run `openspec validate add-ecpay-test-payment --strict`.
- [x] 2.2 Run the cart test suite.
- [ ] 2.3 Smoke test checkout in Docker with an externally reachable callback URL.
