## ADDED Requirements

### Requirement: ECPay Stage Checkout
The system SHALL allow a buyer with a non-empty cart to create an order and continue to the ECPay STAGE hosted payment page.

#### Scenario: Buyer starts payment
- **GIVEN** the buyer has valid cart items and submits valid checkout contact data
- **WHEN** the checkout request is processed
- **THEN** the system creates an order with payment status `pending`
- **AND** the system returns a browser-submitted POST form targeting the ECPay STAGE cashier endpoint
- **AND** the form includes a valid `CheckMacValue`

### Requirement: ECPay Payment Callback Verification
The system SHALL verify ECPay callback data before changing order payment status.

#### Scenario: Successful verified callback
- **GIVEN** an order exists with payment status `pending`
- **WHEN** ECPay posts a callback with a valid `CheckMacValue` and success return code
- **THEN** the system records the ECPay transaction identifiers
- **AND** the system marks the order payment status as `paid`
- **AND** the system responds with ECPay's expected success acknowledgement

#### Scenario: Invalid callback signature
- **GIVEN** an order exists
- **WHEN** ECPay posts a callback with an invalid `CheckMacValue`
- **THEN** the system does not change the order payment status
- **AND** the system logs the verification failure without exposing sensitive customer data

### Requirement: ECPay Payment Configuration
The system SHALL load ECPay endpoint and credential settings from application configuration.

#### Scenario: Development defaults
- **GIVEN** the app runs in development without custom ECPay environment variables
- **WHEN** ECPay settings are read
- **THEN** the system uses the official ECPay STAGE endpoint and public stage test credentials

#### Scenario: Overridden settings
- **GIVEN** ECPay environment variables are configured
- **WHEN** ECPay settings are read
- **THEN** the system uses those configured values instead of development defaults
