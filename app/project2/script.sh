#!/bin/bash          

python /app/project2/manage.py makemigrations tennis
python /app/project2/manage.py migrate
python /app/project2/manage.py loaddata /app/project2/db.json
mod_wsgi-express start-server --port 8000 --working-directory /app/project2 --reload-on-changes /app/project2/project2/wsgi.py
