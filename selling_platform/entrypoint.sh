#!/bin/sh
python manage.py migrate
python manage.py generate_mock_data
exec python manage.py runserver 0.0.0.0:8000
