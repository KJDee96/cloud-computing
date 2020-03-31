#!/bin/bash

apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx

python3.6 -m venv venv

source venv/bin/activate

pip3 install wheel
pip3 install -r requirements.txt
pip3 install uwsgi
flask db upgrade

deactivate

cp cloud-computing.service /etc/systemd/system/cloud-computing.service

systemctl start cloud-computing
systemctl enable cloud-computing

cp cloud-computing /etc/nginx/sites-available/cloud-computing
ln -s /etc/nginx/sites-available/cloud-computing /etc/nginx/sites-enabled

systemctl restart nginx
