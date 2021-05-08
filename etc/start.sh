#!/bin/bash

./manage.py makemigrations
./manage.py migrate --noinput
./manage.py collectstatic --noinput
python3 create_superuser.py
./manage.py runserver 0.0.0.0:4000
