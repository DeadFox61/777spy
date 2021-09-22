#! /bin/bash
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

python send_msgs.py &
python send_msgs_bacc.py &
if [ $DEBUG -eq 1 ] 
then
	python manage.py runserver 0.0.0.0:8000
else
	gunicorn roulette.wsgi --bind 0.0.0.0:8000 --reload --workers=11
fi