# Repository Guidelines

## Project Structure & Module Organization
- Application code lives in `app/`; `app/app.py` builds the Flask app via `create_app` and wires feature blueprints and database init.
- Feature modules sit under `app/features/<name>/` with their own `routes.py` and Jinja templates. Keep new features self-contained to preserve the modular layout.
- Shared utilities (database helpers, error classes) belong in `app/lib/`.
- Static assets are under `app/static/`, while shared layouts and partials reside in `app/templates/`.
- Container and infrastructure assets live in `env/` (Dockerfiles, Nginx config, MySQL seed SQL) alongside `docker-compose.yml` and secret placeholders in `secrets/`.

## Build, Test, and Development Commands
- `docker compose up` — build and start Nginx, Flask, and MySQL with local code mounted. Use `-d` for detached mode during longer sessions.
- `docker compose logs -f flask` — tail application logs; helpful while iterating on routes or templates.
- `docker compose exec flask flask --app app.app routes` — verify registered endpoints after adding or moving blueprints.
- `docker compose down` — stop services and clean up containers; rerun after static asset changes to refresh Nginx cache.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and snake_case for functions, variables, and module names. Keep blueprint instances named `bp` for consistency with existing modules.
- Use type hints as in `create_app` when adding new services or helpers.
- Name templates after their feature (e.g., `app/features/news/templates/news/list.html`) to avoid collisions under `templates/`.
- Store secrets and configuration through the `_read_secret` helper; do not hardcode sensitive values in code or templates.

## Testing Guidelines
- Current workflow relies on manual smoke tests via the running Docker stack. Exercise critical flows (homepage, news, services, contact form) before submitting changes.
- For database-dependent updates, populate fixtures through the SQL scripts in `env/mysql/` or craft targeted insert statements executed with `docker compose exec mysql`.
- Use the `TestingConfig` by setting `APP_ENV=testing` when you need an isolated schema; reset state with `docker compose down -v`.

## Commit & Pull Request Guidelines
- Follow the existing conventional-commit style: lowercase type, optional scope, then a concise summary (e.g., `refactor: reorganize feature templates`).
- Squash noisy work-in-progress commits before opening a PR. Ensure messages describe intent and impact rather than implementation details.
- PRs should include: purpose, notable implementation choices, testing performed (`docker compose up` + manual checks), and screenshots or GIFs when UI changes are visible.
- Link related issues and call out config or secret updates so reviewers can coordinate environment changes.

## Security & Configuration Tips
- Replace the default secrets under `secrets/` before running outside local demos. Keep these files out of version control.
- Use `.env` variables only for non-sensitive overrides; anything secret should flow through Docker secrets and `_read_secret`.
- Avoid logging raw customer input or database credentials; rely on Flask’s logger with contextual messages.
