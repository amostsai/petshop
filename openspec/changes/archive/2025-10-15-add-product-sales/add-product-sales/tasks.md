## 1. Planning
- [x] 1.1 Review existing navigation/header templates to determine catalog entry points.
- [x] 1.2 Finalize database schema additions for products, categories, product_images, orders, and order_items; update `env/mysql/init.sql` diagram.

## 2. Catalog Experience
- [x] 2.1 Create `app/features/products/` blueprint with routes for catalog list and product detail.
- [x] 2.2 Build SQL data access helpers (under `app/lib/` or feature repository) to fetch product lists, categories, and detail records with primary image.
- [x] 2.3 Implement Jinja templates for catalog grid and product detail, including price display and stock messaging.

## 3. Cart & Checkout
- [x] 3.1 Introduce session-backed cart utilities for adding, updating quantity, and removing items.
- [x] 3.2 Implement cart review page showing line items, subtotals, and CTA to checkout.
- [x] 3.3 Add checkout form that collects buyer info, validates input, writes order + order_items to MySQL, and clears the cart.
- [x] 3.4 Render thank-you confirmation with order reference and follow-up instructions.

## 4. Integration & Polish
- [x] 4.1 Update navigation, homepage, and footer links to promote the catalog and featured products.
- [x] 4.2 Seed demo products, categories, and images via `env/mysql/init.sql`; document how to add more items.
- [x] 4.3 Run manual smoke tests (catalog browsing, cart, checkout) and update README with feature overview.
