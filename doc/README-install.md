# Installation and Deployment Plan for REDI

## Prequisities

REDI requires Python 2.7, several python libraries, access to the remote data sources and access to the REDCap system to which it will write the output. In addition, access to the code repository is supplied with git and therefore git must be installed locally.

These libraries are required:

	lxml
	requests

On a mac, run these commands to install the required libraries and related utilities

    sudo easy_install lxml
    sudo easy_install requests
    brew install lftp

In Debian Wheezy, execute these commands

    sudo apt-get install python-lxml
    sudo apt-get install python-requests
    sudo apt-get install lftp

To install git, visit [Git Downloads](http://git-scm.com/downloads) for installation instructions for your operating system. Most linux distributions can install git using their package manager, as in Debian:

    sudo apt-get install git

Note to Mac Users: the deployment scripts below assume the use of GNU Utilities.  The default command line utilities that ship with Mac OSX behave differently.  If you want to use these procedures on a Mac please follow the installation procedures at [GNU Utilities](http://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/) to install the GNU Utilities

## Configuration

REDI is configured via files that appear in ./config/  Once configured these files should be curated with a source control manager like git or mercurial.  

## Deployment to a new installation

Checkout the version of REDI required for this installation

    # set some variables
    redi_git_repository_uri=<redi_git_repository_uri>
    redi_instance_name=<redi_instance_name>

    MYTEMP=`mktemp -d`
    cd $MYTEMP

    git clone $redi_git_repository_uri $redi_instance_name
    sudo mkdir /var/lib/redi.archive/
    sudo mkdir /var/lib/redi/
    sudo cp -r $MYTEMP/$redi_instance_name /var/lib/redi/
    cd /var/lib/redi/$redi_instance_name

    # clean up the mess
    rm -rf $MYTEMP

Copy the example configuration to your home directory for editing and commiting changes.  After editing, this config data needs to be deployed to the production location.

    # set some variables
    redi_instance_configuration_uri=<configuration_URI>

    mkdir ~/$redi_instance_name
    cp -r /var/lib/redi/$redi_instance_name/config-example/* ~/<local_config_folder_name>
    cd ~/$redi_instance_name
    # edit config as needed
    git init 
    git remote add origin $redi_instance_configuration_uri
    git push -u origin master

Deploy config to the REDI instance 

    sudo rm -rf /var/lib/redi/$redi_instance_name/config
    sudo cp -r ~/$redi_instance_name /var/lib/redi/$redi_instance_name/config


## Redeployment to an existing redi installation

Back up existing installation

    # set some variables
    redi_git_repository_uri=<redi_git_repository_uri>
    redi_instance_name=<redi_instance_name>

    date=`date +"%Y%m%d-%H%M"`
    if [ -e /var/lib/redi/$redi_instance_name ];  then
        sudo -E tar czvf   /var/lib/redi.archive/$redi_instance_name.$date.tgz /var/lib/redi/$redi_instance_name
    fi

Remove the existing installation and redeploy code.
Checkout the version of REDI required for this installation

    # clone the master branch into some scratch space
    MYTEMP=`mktemp -d`
    cd $MYTEMP
    # Now checkout the head of master
    git clone $redi_git_repository_uri $redi_instance_name

    # delete the old code
    if [ -e /var/lib/redi/$redi_instance_name ];  then
        sudo rm -rf /var/lib/redi/$redi_instance_name
    fi

    # deploy the new code
    sudo cp -r $MYTEMP/$redi_instance_name /var/lib/redi/
    cd /var/lib/redi/$redi_instance_name
    sudo rm -rf .git

    # Clean up the mess
    rm -rf $MYTEMP

Install the production configuration

    # set some variables
    redi_instance_configuration_uri=<configuration_URI>

    # Clone the config repo to some scratch space
    MYTEMP=`mktemp -d`
    cd $MYTEMP
    git clone $redi_instance_configuration_uri config
    cd config
    rm -rf .git
    cd ..
    
    # Deploy config to the REDI instance
    sudo rm -rf /var/lib/redi/$redi_instance_name/config
    cd $MYTEMP
    sudo cp -r config /var/lib/redi/$redi_instance_name/config

    # Clean up the mess
    cd ~/
    rm -rf $MYTEMP

## Manually run REDI

    # Run script to get EMR data
    sudo /var/lib/redi/$redi_instance_name/config/getEmrData.sh
    # Run REDI
    sudo python /var/lib/redi/$redi_instance_name/bin/redi.py

## Configure this REDI to run via cron


