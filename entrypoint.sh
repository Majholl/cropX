#!/bin/bash

set -e 

echo "Running django migrations"

python3 manage.py makemigrations
python manage.py collectstatic
python3 manage.py migrate 

echo "Starting django server"

python3 manage.py runserver 0.0.0.0:8000