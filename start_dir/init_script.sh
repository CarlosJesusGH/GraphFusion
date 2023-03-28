#!/bin/bash

# exit when any command fails
set -e

git_repo=$1;
DIR="/home/iconbi_graphcrunch/"
if [ -d "$DIR" ]; then
### Take action if $DIR exists ###
cd /home/iconbi_graphcrunch/
git reset --hard origin/master
git pull
else
###  Control will jump here if $DIR does NOT exists ###
git clone $git_repo
mv iconbi-graphcrunch iconbi_graphcrunch
fi
conda deactivate
source /home/Downloads/GC3-WWW/www/GC3Env/bin/activate
cd /home/iconbi_graphcrunch/WebServer
# service mysql start
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000