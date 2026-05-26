## Why
Customers can currently submit an order, but there is no online payment step. Adding ECPay test payment lets the shop validate the hosted payment flow before moving to production credentials.

## What Changes
- Add ECPay All-in-One payment integration using the STAGE endpoint.
- Generate ECPay checkout form parameters and CheckMacValue from server-side order data.
- Redirect buyers from checkout to the ECPay hosted payment page after the order is created.
- Receive and verify ECPay payment result callbacks, then update the order payment status.
- Add configuration for ECPay endpoint, MerchantID, HashKey, HashIV, and callback URLs.

## Impact
- Affected specs: ecpay-payment
- Affected code: `app/config.py`, `app/features/cart/`, `env/mysql/init.sql`, cart tests
- Data impact: `orders` needs payment status and ECPay transaction tracking fields.
