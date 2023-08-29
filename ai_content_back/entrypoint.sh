python manage.py wait_for_db
python manage.py migrate --no-input
python manage.py collectstatic --no-input


if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_USERNAME
fi

$@


gunicorn aicontent.wsgi -w 4 -b 0.0.0.0:8000