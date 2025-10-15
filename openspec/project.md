# Project Context

## Purpose
`petshop` hosts the 「毛孩樂園」 pet store demo site. It showcases a modular Flask application that renders marketing content (home, services, news, about) and captures contact form submissions backed by MySQL. The project serves as a learning sandbox for full-stack development and containerized deployment with Nginx as the public entry point.

## Tech Stack
- Python 3.11 with Flask 3.1.1 using the application factory pattern and Blueprints
- Jinja2 3.1 templates for server-rendered pages and shared layouts
- MySQL 8.0 seeded via `env/mysql/init.sql` for news, services, and contact data
- Nginx (alpine) reverse proxy that also serves static assets from `app/static`
- Docker Compose to orchestrate the Flask, MySQL, and Nginx services locally

## Project Conventions

### Code Style
- Follow PEP 8 with 4-space indentation, snake_case identifiers, and concise helper functions.
- Keep each feature Blueprint instance named `bp`; expose blueprints through module-level `bp` for registration.
- Store shared helpers (DB access, secrets, custom errors) under `app/lib/`; avoid duplicating logic inside features.
- Read secrets via `_read_secret` and environment variables—never hardcode sensitive values or credentials.

### Architecture Patterns
- `app/app.py` provides `create_app`, wires blueprints, and initializes MySQL connections. Treat it as the single application entry point.
- Features live under `app/features/<name>/` with their own `routes.py` and scoped templates; prefer adding services/repositories inside the same folder when behavior grows.
- Shared templates belong in `app/templates/`; static assets stay under `app/static/` so Nginx can serve them directly.
- Docker Compose defines the three-tier stack (Nginx → Flask → MySQL) and mounts source code into the Flask container for live reloads.

### Testing Strategy
- Primary validation is manual smoke testing after `docker compose up`: exercise homepage, news listing, services page, and contact form flows.
- When changing database-backed features, update `env/mysql/init.sql` or craft targeted inserts via `docker compose exec mysql`.
- Use `APP_ENV=testing` to load `TestingConfig` and isolate schema when deeper verification is required; tear down with `docker compose down -v`.
- Watch Flask logs with `docker compose logs -f flask` during manual testing to confirm routes and DB calls behave as expected.

### Git Workflow
- Use conventional commits (`type: summary`, optional scope) and squash noisy WIP commits before opening PRs.
- Develop on feature branches forked from the main line; keep changes scoped to one feature module whenever possible.
- Document PRs with purpose, notable decisions, manual testing evidence (screenshots for UI changes), and call out config or secret updates.

## Domain Context
- The site represents a Taiwan-based pet shop offering grooming, boarding, and adoption guidance. Content is mostly static marketing copy in Traditional Chinese sourced from seed data.
- Core pages include: landing (`features/main`), services (`features/services`), news/blog (`features/news`), about (`features/about`), and a contact form (`features/contact`) that persists submissions to MySQL.
- Visual assets are illustrative placeholders pulled from the web; replace them before any production deployment.

## Important Constraints
- Secrets are mounted from the `secrets/` directory via Docker secrets; replace defaults before sharing or deploying environments.
- Static asset changes require recycling Nginx (`docker compose down && docker compose up`) to bypass caching.
- Do not log raw sensitive input (contact messages, credentials); rely on Flask’s structured logging.
- Containers assume the Asia/Taipei timezone and local development usage—no baked-in scaling or HA provisions.

## External Dependencies
- Docker Hub images: `python:3.11-slim`, `mysql:8.0`, and `nginx:alpine`.
- Python packages `mysql-connector-python` and `Jinja2` pulled via `env/flask/requirements.txt`.
- MySQL server seeded from `env/mysql/init.sql`; no third-party APIs are consumed today.
