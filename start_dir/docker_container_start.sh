#!/bin/bash
cd /home/iconbi_graphcrunch/
git reset --hard origin/master
git pull
cd WebServer/
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000
