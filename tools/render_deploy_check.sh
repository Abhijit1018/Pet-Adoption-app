#!/bin/bash
set -e

echo "=== Environment variables summary ==="
# Print whether key env vars are set (do not print secrets)
[ -n "$DATABASE_URL" ] && echo "DATABASE_URL=SET" || echo "DATABASE_URL=NOT SET"
[ -n "$CHAT_DATABASE_URL" ] && echo "CHAT_DATABASE_URL=SET" || echo "CHAT_DATABASE_URL=NOT SET"
[ -n "$MYSQL_DATABASE" ] && echo "MYSQL_DATABASE=SET" || echo "MYSQL_DATABASE=NOT SET"
[ -n "$MYSQL_USER" ] && echo "MYSQL_USER=SET" || echo "MYSQL_USER=NOT SET"
[ -n "$MYSQL_PASSWORD" ] && echo "MYSQL_PASSWORD=SET" || echo "MYSQL_PASSWORD=NOT SET"
[ -n "$SECRET_KEY" ] && echo "SECRET_KEY=SET" || echo "SECRET_KEY=NOT SET"
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"
echo "DEBUG=$DEBUG"

echo "\n=== Django check ==="
python manage.py check || true

echo "\n=== Migrations ==="
python manage.py migrate --noinput

echo "\n=== Collectstatic ==="
python manage.py collectstatic --noinput

echo "\n=== Completed deploy check ==="
