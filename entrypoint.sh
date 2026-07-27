#!/bin/sh

while ! nc -z db 5432; do
	sleep 1
done

echo "postgres is ok"

python manage.py migrate

exec "$@"
