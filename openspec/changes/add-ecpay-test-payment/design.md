## Context
The cart flow already validates inventory, creates an order, stores order items, clears the cart, and redirects to a local thank-you page. ECPay All-in-One payment expects a browser-submitted POST form to the hosted payment endpoint. The test environment uses the stage cashier URL and test credentials.

## Goals / Non-Goals
- Goals: support ECPay STAGE hosted payment for existing cart orders, verify CheckMacValue on callbacks, and persist payment outcome.
- Non-Goals: production credential rollout, refunds, partial captures, logistics integration, invoice integration, or admin order management.

## Decisions
- Keep the integration inside the cart feature because checkout and order persistence already live there.
- Add a focused payment helper module for parameter generation and CheckMacValue verification so route handlers stay small.
- Create orders before redirecting to ECPay and mark them `pending` until a valid callback is received.
- Continue using the current database seed script for schema changes, matching the repository's local-development workflow.
- Use environment/config values for all ECPay settings. Development defaults may use official stage test credentials only because they are public test values; production must override them.

## External References
- ECPay stage endpoint: `https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5`
- Official stage test MerchantID: `3002607`
- Official stage test HashKey: `pwFHCqoQZGmho4w6`
- Official stage test HashIV: `EkRm7iFT261dpevs`

## Risks
- ECPay server-to-server callback requires a public ReturnURL. Local Docker-only testing needs a tunnel such as ngrok or a deployed test host.
- Duplicate callbacks can occur, so updates must be idempotent by order number.
- Order numbers sent as `MerchantTradeNo` must stay within ECPay's length and character constraints.
