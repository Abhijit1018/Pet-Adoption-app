Render deployment steps for Pet Adoption & Rescue Management Portal

1) Prepare the repository
- Ensure code is pushed to a branch on GitHub (we used `Abhijit_Singh_local_push`).
- Add this repository to Render via "New -> Web Service" and connect GitHub.
- Use the `render.yaml` blueprint or set service options manually.

2) Environment variables (set in Render Dashboard -> Environment)
- `DJANGO_SETTINGS_MODULE=home.settings`
- `SECRET_KEY` -> set a secure random value
- `DATABASE_URL` -> set to the Render Postgres DB or external DB (recommended)
- `ALLOWED_HOSTS` -> set to your site domain or `*` for testing
- Optional: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` etc.

3) Python packages & static files
- `render.yaml` uses `pip install -r requirements.txt` during build.
- Static files: the buildCommand runs `python manage.py collectstatic --noinput`. Ensure `STATIC_ROOT` is configured in `home/settings.py`.

4) Database migrations
- After the service deploys, run migrations via Render shell or by adding a one-time deploy command:
  - `python manage.py migrate`
  - `python manage.py migrate --database=chat_db` (to create chat DB tables if using persistent DB)

5) Chat DB considerations
- Local development used a sqlite `chat_db.sqlite3`. For production, you should use a managed Postgres DB and update `home/settings.py` DATABASES to include a chat DB entry using the production DATABASE_URL(s).
- Alternatively, you can merge chat tables into the primary DB but that requires refactoring (removing cross-DB safe guards).

6) Post-deploy
- Create a superuser: `python manage.py createsuperuser` (via Render shell)
- Verify email configuration and other services.

7) Notes
- We added `.gitignore` to prevent committing `db.sqlite3`, `chat_db.sqlite3`, venvs, and compiled files.
- CI: add GitHub Actions or Render webhooks to run tests before deploy.

If you want, I can:
- Update `home/settings.py` with production-friendly DB setup templates (using `dj-database-url`).
- Add a simple `Procfile` (already added) and a systemd/gunicorn config sample.
- Move chat DB to Postgres and update code to use `.using('chat_db')` with Postgres (I can scaffold migrations).
