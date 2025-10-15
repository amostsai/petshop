## Why
- Route coverage currently relies on manual smoke testing; we lack automated verification that key blueprints render successfully after changes.
- Adding pytest suites will improve confidence when extending features like products and cart, catching regressions before manual QA.
- Establishing reusable testing fixtures will accelerate future contributions and documentation around the testing workflow.

## What Changes
- Introduce a pytest setup (configuration, fixtures) that spins up the Flask app with `TestingConfig` and uses a temporary MySQL schema or in-memory substitute.
- Author smoke-test modules for each feature blueprint (`about`, `cart`, `contact`, `main`, `news`, `products`, `services`) that validate primary routes, template rendering, and critical behaviors (e.g., POST contact submission, cart session usage).
- Seed deterministic test data for products/news/services either via fixtures or dedicated helper functions so tests execute without relying on production seed scripts.
- Update developer documentation to describe running `pytest`, managing the test database, and expectations for contributing new tests.

## Impact
- Adds pytest (and supporting libraries such as `pytest-flask` or `faker`) to the development dependencies.
- Requires wiring temporary storage (sqlite or disposable MySQL schema) to keep tests isolated from local data.
- Increases CI runtime; if CI is configured later, the new test suite must be executed.
