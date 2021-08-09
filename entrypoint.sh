#! /bin/bash

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

python send_msgs.py &
python send_msgs_bacc.py &
python manage.py runserver 0.0.0.0:8000
