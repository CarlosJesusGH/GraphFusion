#!/usr/bin/env bash

source ../../bin/activate
service apache2 stop
git pull
# ./update_dependencies.sh
mv ./logs/log.log ./logs/log.log.temp
touch ./logs/log.log
./update_database.sh
mv ./logs/log.log ./logs/deploy.log
mv ./logs/log.log.temp ./logs/log.log
#setting correct permissions
# if [ -f ./set_permissions.sh ]; then
#     ./set_permissions.sh
# fi
service apache2 start
deactivate
