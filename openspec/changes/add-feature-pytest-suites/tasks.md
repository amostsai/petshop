## 1. Test Infrastructure
- [x] 1.1 Add pytest tooling to the project (dependency entry, `pytest.ini` defaults, `.coveragerc` if needed).
- [x] 1.2 Create `conftest.py` fixtures that instantiate the Flask app with `TestingConfig`, initialize a temporary database, and provide a test client.
- [x] 1.3 Document how to run tests with optional environment variables (e.g., `APP_ENV=testing`) and any required setup.

## 2. Feature Smoke Tests
- [x] 2.1 Implement `tests/features/test_main.py` validating the homepage renders and contains latest news/services snippets.
- [x] 2.2 Add `tests/features/test_news.py` covering list and detail routes (including 404 path).
- [x] 2.3 Add `tests/features/test_services.py` ensuring services page returns 200 and displays seeded services.
- [x] 2.4 Add `tests/features/test_about.py` verifying about route renders expected content.
- [x] 2.5 Add `tests/features/test_contact.py` covering GET form rendering and successful POST submission persistence.
- [x] 2.6 Add `tests/features/test_products.py` covering catalog, category filter, and product detail flows.
- [x] 2.7 Add `tests/features/test_cart.py` exercising add/update/remove endpoints and checkout happy path.

## 3. Data & Utility Fixtures
- [x] 3.1 Create helper fixtures/factories for seeding news, services, products, orders within tests.
- [x] 3.2 Ensure fixtures clean up between tests, resetting database state (transaction rollbacks or truncation).

## 4. Documentation & Tooling
- [x] 4.1 Update README / project docs with pytest instructions and expectations for maintaining test coverage.
- [x] 4.2 (Optional) Wire pytest into Makefile or `docker compose` helper command to encourage usage.
