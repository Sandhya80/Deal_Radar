web: gunicorn deal_radar.wsgi:application --log-file -
release: python manage.py collectstatic --noinput && python manage.py migrate --noinput