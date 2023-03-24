#!/bin/bash
echo "execute this script with 'source' rather than 'bash'"
cd /home/iconbi_graphcrunch/
git pull
cd GC3_WebServer/
service mysql restart
mysql --execute="SHOW DATABASES;"
conda activate GC3Env
python manage.py runserver 0.0.0.0:8000
