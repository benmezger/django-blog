#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

mkdir -p /usr/src/logs
mkdir -p /usr/src/app/src/static
mkdir -p /usr/src/app/src/assets

# Prepare log files and start outputting logs to stdout
touch /usr/src/logs/gunicorn.log
touch /usr/src/logs/access.log
tail -n 0 -f /usr/src/logs/*.log &

if [ "$ENV" = "development" ] ; then
    python docker/web/check_db.py --service-name Postgres --ip db --port 5432
fi

python manage.py migrate
python manage.py collectstatic --noinput  # Collect static files

echo Starting Gunicorn.
if [ "$ENV" = "development" ] ; then
    pipenv install --dev --system
    exec gunicorn --reload benmezger.wsgi --bind 0.0.0.0:8000
else
    (exec gunicorn benmezger.wsgi \
         --name core \
         --bind 0.0.0.0:8000 \
         --workers 3 \
         --timeout 120 \
         --worker-class gevent \
         --log-level=info \
         --log-file=/usr/src/logs/gunicorn.log \
         --access-logfile=/usr/src/logs/access.log \
         "$@")
fi
