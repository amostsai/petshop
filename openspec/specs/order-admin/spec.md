# order-admin Specification

## Purpose
TBD - created by archiving change add-order-admin. Update Purpose after archive.
## Requirements
### Requirement: Protected Order Admin Access
The system SHALL restrict order administration pages to authenticated staff users.

#### Scenario: Anonymous visitor opens admin orders
- **GIVEN** a visitor is not authenticated as staff
- **WHEN** they request the order admin list
- **THEN** the system redirects them to the admin login page

#### Scenario: Staff logs in with configured credentials
- **GIVEN** admin credentials are configured
- **WHEN** staff submit matching credentials
- **THEN** the system creates an admin session
- **AND** redirects them to the order admin list

### Requirement: Order List With Payment Filters
The system SHALL provide a staff-facing list of orders with payment status filters.

#### Scenario: Staff filters pending orders
- **GIVEN** staff are authenticated
- **WHEN** they open the order list filtered by `pending`
- **THEN** the system shows only orders whose payment status is `pending`
- **AND** each row shows order number, customer name, total amount, created time, and payment status

#### Scenario: Staff filters paid orders
- **GIVEN** staff are authenticated
- **WHEN** they open the order list filtered by `paid`
- **THEN** the system shows only orders whose payment status is `paid`

#### Scenario: Staff filters failed or cancelled orders
- **GIVEN** staff are authenticated
- **WHEN** they choose `failed` or `cancelled`
- **THEN** the system shows only orders matching the selected status

### Requirement: Order Detail Review
The system SHALL provide an order detail page for staff review.

#### Scenario: Staff opens an order detail
- **GIVEN** staff are authenticated
- **WHEN** they open an existing order detail page
- **THEN** the system shows customer contact fields, fulfillment method, notes, order items, total amount, payment status, and available ECPay transaction fields

#### Scenario: Staff opens a missing order
- **GIVEN** staff are authenticated
- **WHEN** they open a non-existent order number
- **THEN** the system returns a not found response

### Requirement: Local Order Cancellation
The system SHALL allow staff to locally cancel orders that are not paid.

#### Scenario: Staff cancels an unpaid order
- **GIVEN** staff are authenticated
- **AND** an order has payment status `pending` or `failed`
- **WHEN** staff submit the cancel action
- **THEN** the system marks the order as `cancelled`
- **AND** returns staff to the order detail page with a confirmation message

#### Scenario: Staff attempts to cancel a paid order
- **GIVEN** staff are authenticated
- **AND** an order has payment status `paid`
- **WHEN** staff submit the cancel action
- **THEN** the system does not change the order status
- **AND** informs staff that paid orders cannot be cancelled locally

### Requirement: Cancelled Order Callback Handling
The system SHALL preserve a locally cancelled order when a later ECPay callback arrives unless a future spec defines reconciliation behavior.

#### Scenario: ECPay callback arrives for cancelled order
- **GIVEN** an order has payment status `cancelled`
- **WHEN** a verified ECPay callback arrives for that order
- **THEN** the system does not change the payment status to `paid`
- **AND** records or logs that the callback was ignored because the order was already cancelled

