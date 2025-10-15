## Why
- Expand the 毛孩樂園 demo into a fuller pet shop experience by letting visitors browse and purchase merchandise (food, accessories, grooming products).
- Demonstrate data-driven pages beyond static marketing content and extend MySQL usage with product and order persistence.
- Serve as a learning reference for session-backed cart flows and order submission handling within the existing Flask + Nginx + MySQL stack.

## What Changes
- Introduce a catalog blueprint with list and detail pages that render products from new MySQL tables (products, categories, product_images).
- Add a lightweight shopping cart stored in the user session that supports adding, updating, and removing product line items.
- Implement a checkout flow that captures buyer contact info, summarizes cart contents, writes orders/order_items to MySQL, and surfaces a thank-you screen.
- Surface navigation and homepage entry points so the new product catalog integrates with the current marketing site experience.
- Extend seed data and admin SQL scripts to populate sample products for local demos.

## Impact
- Requires new MySQL schema objects and migrations/seed inserts (deployed through `env/mysql/init.sql`).
- Adds new blueprints, templates, forms, and session usage that will increase Flask routing complexity.
- Will require documentation updates (README, navigation instructions) and manual smoke testing across product, cart, and checkout flows.
