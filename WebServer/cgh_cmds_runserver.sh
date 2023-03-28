#!/bin/bash

# check updated info in file:
# file:///home/bscuser/Dropbox/Personal/Study/BSC/05_GraphCrunch3/run_gc3_into_container/docker_commands.md
# the following is basically a copy-paste from that file.

input_var=$1;
git_repo=$2;

# if [ $input_var -eq 0 ]
if [[ -z $input_var ]]
then
  echo "No arguments supplied, assuming 'host'";
  input_var='host';
fi

echo "input_var="$input_var;

if [ $input_var == "host" ]
then
  echo "into 'host'"
  source deactivate
  echo "entering container, next do:"
  echo "  bash /home/Downloads/GC3-WWW/www/GC3Env/GC3/WebServer/cgh_cmds_runserver.sh container"
  docker container start gc3_cont_v220523 
  echo "container started, if want a detached bash session on a different terminal, do:"
  echo "  docker exec -it gc3_cont_v220523 bash"
  docker container attach gc3_cont_v220523
elif [ $input_var == 'container' ]
then
  cd /home/Downloads/GC3-WWW/www/GC3Env/GC3/WebServer
  conda deactivate
  source ../../bin/activate
  service mysql start
  python manage.py runserver 0.0.0.0:8000
elif [ $input_var == 'container_nosource' ]
then
  # git_repo=$1;
  DIR="/home/iconbi_graphcrunch/"
  if [ -d "$DIR" ]; then
    ### Take action if $DIR exists ###
    cd /home/iconbi_graphcrunch/
    git reset --hard origin/master
    git pull
  else
    ###  Control will jump here if $DIR does NOT exists ###
    git clone $git_repo
  fi
  conda deactivate
  source /home/Downloads/GC3-WWW/www/GC3Env/bin/activate
  cd /home/iconbi_graphcrunch/WebServer
  # service mysql start
  service mysql restart
  mysql --execute="SHOW DATABASES;"
  python manage.py runserver 0.0.0.0:8000
else
  echo "argument is not valid"
fi