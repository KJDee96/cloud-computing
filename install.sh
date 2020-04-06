#!/bin/bash

apt -y update
apt -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx awscli

echo "DATABASE_URI=\"postgresql://imagedbuser:jM4A7X0s7mFX@us-east-1-rds.cf0oovcnacdx.us-east-1.rds.amazonaws.com:5432/uploads\"" >> /etc/environment
echo "BUCKET=\"us-east-1-image-bucket\"" >> /etc/environment
echo "CLOUDFRONT=\"dmwtvmrtya2b7.cloudfront.net\"" >> /etc/environment

pip3 install git-remote-codecommit

mkdir /root/.aws
cd /root/.aws
echo "[default]
aws_access_key_id = AKIA5HUWTH575GDDVLUV
aws_secret_access_key = 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" > credentials

echo "[default]
region = us-east-1" > config

cd /var/www/

git clone codecommit::us-east-1://cloud-computing

cd cloud-computing

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

rm /etc/nginx/sites-enabled/default

systemctl restart nginx