#!/bin/sh
sudo add-apt-repository "deb http://apt.nuxeo.org/ trusty releases"
wget -q -O- http://apt.nuxeo.org/nuxeo.key | sudo apt-key add -

echo "nuxeo nuxeo/http-port string 8080" | sudo debconf-set-selections
echo "nuxeo nuxeo/bind-address string 0.0.0.0" | sudo debconf-set-selections
echo "nuxeo nuxeo/database select PostgreSQL" | sudo debconf-set-selections

export DEBIAN_FRONTEND=noninteractive
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8

sudo apt-get update
sudo apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" nuxeo=6.0-01
sudo apt-get install -y python-pip

cd /vagrant
sudo -H pip install -r requirements.txt

ansible-playbook package_example.yml -i 'localhost,' --connection=local
