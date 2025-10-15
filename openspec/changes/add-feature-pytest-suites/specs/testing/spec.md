## ADDED Requirements

### Requirement: Feature Blueprints Have Smoke Tests
Pytest suites MUST exercise each registered blueprint to confirm primary routes render successfully with seeded data.

#### Scenario: main homepage renders
- **GIVEN** the test database contains seed news and services
- **WHEN** the pytest client requests `/`
- **THEN** the response status is 200
- **AND** the HTML includes at least one news title and one service name

#### Scenario: news list and detail
- **GIVEN** the test database contains at least one news record
- **WHEN** the pytest client requests `/news` and `/news/<id>`
- **THEN** both responses return 200 with the expected news title
- **AND** a request to `/news/99999` returns 404

#### Scenario: services page
- **WHEN** the pytest client requests `/services`
- **THEN** the response status is 200 and contains the seeded service descriptions

#### Scenario: about page
- **WHEN** the pytest client requests `/about`
- **THEN** the response status is 200 and includes the about content copy

#### Scenario: contact form get/post
- **WHEN** the pytest client requests `/contact`
- **THEN** the response status is 200
- **AND** submitting the contact form with valid payload returns a redirect and persists the entry for later assertions

#### Scenario: product catalog and detail
- **GIVEN** the test database is populated with products and categories
- **WHEN** the pytest client requests `/products`, `/products?category=<slug>`, and `/products/<slug>`
- **THEN** each response returns 200 and the catalog filter narrows results to the matching category

### Requirement: Cart And Checkout Flow Are Tested
Pytest suites MUST cover cart mutation endpoints and checkout order creation using session state.

#### Scenario: cart lifecycle
- **WHEN** the pytest client posts to `/cart/add`, `/cart/update`, and `/cart/remove` with valid product references
- **THEN** the responses redirect successfully
- **AND** the cart summary reflects the expected item counts after each operation

#### Scenario: checkout persistence
- **GIVEN** the cart contains at least one in-stock item
- **WHEN** the pytest client submits the checkout form
- **THEN** the response redirects to a thank-you page
- **AND** the test database records an order with associated order_items containing the cart line items
