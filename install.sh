#!/bin/bash

# apt update and install requirements
apt -y update
apt -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx awscli

# aws codecommit requirement
pip3 install git-remote-codecommit

# set up aws credentials
mkdir /root/.aws
cd /root/.aws
echo "[default]
aws_access_key_id = ""
aws_secret_access_key = "" > credentials

echo "[default]
region = us-east-1" > config

# clone project
cd /var/www/
git clone codecommit::us-east-1://cloud-computing
cd cloud-computing

# set up virtual env
python3.6 -m venv venv

source venv/bin/activate

pip3 install wheel
pip3 install -r requirements.txt
pip3 install uwsgi
flask db upgrade

deactivate

# create cloud-computing systemd service
cp cloud-computing.service /etc/systemd/system/cloud-computing.service

# remove default nginx site
rm /etc/nginx/sites-enabled/default

# enable nginx site
cp cloud-computing /etc/nginx/sites-available/cloud-computing
ln -s /etc/nginx/sites-available/cloud-computing /etc/nginx/sites-enabled

# run metadata tool to pull data for debug page
ec2metadata >> instance_data

# restart services
systemctl start cloud-computing
systemctl enable cloud-computing
systemctl restart nginx
