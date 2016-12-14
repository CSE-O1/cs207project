#!/bin/sh
sudo pkill -f httpd
sudo pkill -f python3



sudo rm /etc/nginx/sites-enabled/*
sudo rm /etc/nginx/sites-available/app_server_nginx.conf
sudo rm /etc/nginx/sites-available/api_server_nginx.conf
sudo cp scripts/app_server_nginx.conf /etc/nginx/sites-available/
sudo rm /etc/nginx/sites-enabled/app_server_nginx.conf
sudo ln -s /etc/nginx/sites-available/app_server_nginx.conf /etc/nginx/sites-enabled/app_server_nginx.conf
sudo service nginx restart


sudo rm -r /home/www
sudo mkdir /home/www
cd ..
sudo cp -R cs207project /home/www/
cd /home/www/cs207project
sudo chmod 777 vpDB/*
sudo chmod 777 data/*
export FLASK_APP=./frontend/view.py
PYTHONPATH=./ python3 server/DBServer.py 50000 &
PYTHONPATH=./ python3 -m frontend.view
flask run

