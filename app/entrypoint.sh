#!/bin/sh

# Ждать пока запуститься БД
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input  # Удаление данных из таблиц
# python manage.py migrate  # Миграция бд

exec "$@"