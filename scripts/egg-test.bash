#!/usr/bin/env bash

# Tests redi from an EGG installation within a virtualenv sandbox

VIRTUALENV_NAME=venv

# Path of the directory containing this script
DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REDI_ROOT="$( cd $DIRNAME/.. && pwd)"
VIRTUALENV_DIR=$REDI_ROOT/$VIRTUALENV_NAME

# Check to see if virtualenv is installed
which virtualenv || sudo easy_install virtualenv
if [ ! -d $REDI_ROOT/config ]; then
	echo ERROR! Missing config directory at $REDI_ROOT/config
	exit 1
fi

# Clean up from a previous run
rm -rf $VIRTUALENV_DIR

# Create virtual python environment, install the EGG, run redi, and cleanup.
virtualenv $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pushd $REDI_ROOT
make
# Workaround to install lxml on some OS X boxes
ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future \
	make install

redi -c $REDI_ROOT/config
popd

deactivate
rm -rf $VIRTUALENV_DIR

