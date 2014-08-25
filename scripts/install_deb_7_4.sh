#!/bin/bash

# Installation script for Debian 7.4
#
# Note: you can run this script non-interactively like so:
#     $ sudo DEBIAN_FRONTEND=noninteractive ./install_deb_7_4.sh

if [[ $EUID -ne 0 ]]; then
	echo "You need to run this script as root" 2>&1
	exit 1
fi

apt-get update
apt-get -y install python-setuptools libxml2 libxslt1-dev python-dev
easy_install REDI-0.11.0-py2.7.egg
