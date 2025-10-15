## ADDED Requirements

### Requirement: Browse Pet Products
Visitors MUST be able to view the available product catalog with category filtering.

#### Scenario: view catalog grid
- **GIVEN** at least one product is published
- **WHEN** a visitor opens `/products`
- **THEN** the page lists products with name, thumbnail, price, and category tags
- **AND** the visitor can filter the list by category without leaving the page

### Requirement: View Product Detail
Visitors MUST be able to inspect individual product details and see purchase availability.

#### Scenario: show product information
- **GIVEN** a product has at least one image and description
- **WHEN** a visitor opens `/products/<slug>`
- **THEN** the page renders title, gallery image, long description, price, and stock status
- **AND** an add-to-cart control is visible when the product is in stock

### Requirement: Manage Shopping Cart
Visitors MUST be able to add products to a cart, adjust quantities, and review totals stored in their session.

#### Scenario: adjust cart line items
- **GIVEN** a visitor has added a product to the cart
- **WHEN** they navigate to `/cart`
- **THEN** each line item shows name, selected quantity, unit price, and line subtotal
- **AND** the visitor can update quantity or remove the item and see the cart totals refresh

### Requirement: Submit Product Order
Visitors MUST be able to provide contact information, confirm their cart, and submit an order captured in MySQL.

#### Scenario: complete checkout
- **GIVEN** the visitor has a non-empty cart
- **WHEN** they submit the checkout form with valid name, email, phone, and pickup/delivery preference
- **THEN** an order record with associated order_items is persisted to MySQL
- **AND** the cart is cleared and a confirmation page with order reference is displayed
