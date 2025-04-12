#!/bin/sh 

set -e

echo "Running migrations"

python3 manage.py makemigrations 
python3 manage.py migrate


echo "Running Server"
exec python3 manage.py runserver 0.0.0.0:8010