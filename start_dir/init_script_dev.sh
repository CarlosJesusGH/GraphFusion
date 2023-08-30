#!/bin/bash

# exit when any command fails
set -e

source /root/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate GC3Env
cd /home/GraphFusion_host/WebServer
service mysql restart
mysql --execute="SHOW DATABASES;"
python manage.py runserver 0.0.0.0:8000