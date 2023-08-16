#!/bin/bash

# exit when any command fails
set -e

# git_repo=$1;
git_repo="https://github.com/CarlosJesusGH/GraphFusion.git"
DIR="/home/GraphFusion/"
if [ -d "$DIR" ]; then
### Take action if $DIR exists ###
cd /home/GraphFusion/
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
cd /home/GraphFusion/WebServer
# service mysql start
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000

# when running locally for developement
# docker run -it --rm -p 8000:8000 -v /home/bscuser/repos/GraphFusion:/home/GraphFusion_host --entrypoint bash carlosjesusgh/graphfusion:latest
# re-make init_script.sh (rm init_script.sh && nano init_script.sh) and add the following lines:
<<lines_to_add
!/bin/bash
set -e
source /root/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate GC3Env
cd /home/GraphFusion_host/WebServer
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000
lines_to_add
# run init_script.sh
  # chmod 777 init_script.sh && ./init_script.sh

