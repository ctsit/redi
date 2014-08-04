#!/usr/bin/env bash

# Tests redi from an EGG installation within a virtualenv sandbox

VIRTUALENV_DIR=venv

# Path of the directory containing this script
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check to see if virtualenv is installed
which virtualenv || sudo easy_install virtualenv
[ -d $ROOT/../config ] || echo "ERROR! Missing config directory"; exit 1

# Clean up from a previous run
cd $ROOT/..
rm -rf $VIRTUALENV_DIR

# Create virtual python environment, install the EGG, run redi, and cleanup.
virtualenv $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate
# Workaround to install lxml on OS X
ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future easy_install \
	$ROOT/../dist/REDI*egg
redi -c $ROOT/../config
deactivate
rm -rf $VIRTUALENV_DIR

