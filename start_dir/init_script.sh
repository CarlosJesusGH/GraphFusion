#!/bin/bash

# exit when any command fails
set -e

# git_repo=$1;
git_repo="https://github.com/CarlosJesusGH/GraphFusion.git"
DIR="/home/graphfusion/"
if [ -d "$DIR" ]; then
### Take action if $DIR exists ###
cd /home/graphfusion/
git reset --hard origin/master
git pull
else
###  Control will jump here if $DIR does NOT exists ###
git clone $git_repo
fi
# instead of conda init + logout/login
source /root/miniconda3/etc/profile.d/conda.sh
conda deactivate
#source /home/Downloads/GC3-WWW/www/GC3Env/bin/activate
conda activate GC3Env
cd /home/graphfusion/WebServer
# service mysql start
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000