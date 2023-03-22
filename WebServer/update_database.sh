#!/usr/bin/env bash
./manage.py makemigrations --setting=WebServer.settings_prod
./manage.py migrate --setting=WebServer.settings_prod
./manage.py syncdb --setting=WebServer.settings_prod