#!/bin/bash

/app/wait-for-it.sh -t 60 -h $MYSQL_HOST -p $MYSQL_PORT

cd ./email_parser
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver "0.0.0.0:$PORT"