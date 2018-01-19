#!/usr/bin/bash

sudo yum -q -y update
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm

sudo yum -q -y update

sudo yum -y install python36u redis
sudo systemctl start redis

wget -q https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
rm get-pip.py

sudo pip install django
sudo pip install -U "celery[redis]"
sudo pip install ipython requests
