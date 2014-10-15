Testing RED-I with a sample REDCap Project
==========================================

Purpose
-------

The "vagrant" folder was created with the goal of making testing `RED-I
software <https://github.com/ctsit/redi>`__ as easy as possible. It
contains the `Vagrantfile <../vagrant/Vagrantfile>`__ which allows you to
start a virtual machine capable of running the `REDCap
software <http://http://www.project-redcap.org>`__ -- which means that
during virtual machine creation the Apache and MySQL software is
installed without any user intervention.

There are a few important things to note before proceeding with running
RED-I to import data into a sample REDCap project:

-  You have to install the **vagrant** and **virtual box** software
-  You have to obtain the closed-source REDCap software from
   http://project-redcap.org/
-  You have to obtain a **Makefile.ini** file in order to be able to
   execute tasks from the **Makefile**

Steps
-----

1. Install vagrant and virtual box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a linux machine run:

-  sudo apt-get install vagrant
-  sudo apt-get install virtualbox

On a mac machine:

-  Download and install vagrant from
   https://www.vagrantup.com/downloads.html
-  Download and install the latest virtual box from
   http://download.virtualbox.org/virtualbox/

For more details about Vagrant software you can go to
`why-vagrant <https://docs.vagrantup.com/v2/why-vagrant/>`__ page.

2. Configure the VM
~~~~~~~~~~~~~~~~~~~

As mentioned above you have to obtain a copy of the REDCap software from
http://project-redcap.org/ and save it as "**redcap.zip**\ " file in the
"**config-example/vagrant-data**\ " folder. This ensures that in the
later steps the `bootstrap.sh <../vagrant/bootstrap.sh>`__ script can
extract the files to the virtual machine path "**/var/www/redcap**\ ".

Now execute the following commands to complete the configuration:

.. raw:: html

   <pre>
   cd ./vagrant    # must be in the redi/vagrant/ directory
   make copy_config_example
   make copy_redcap_code
   make copy_project_data
   make show_config
   </pre>

Please verify that the output from "show\_config" matches your
expectations.

3. Start the VM
~~~~~~~~~~~~~~~

To use the vagrant VM you will need to install Vagrant and Virtual Box.

With these packages installed, follow this procedure to use a VM
template:

.. raw:: html

   <pre>
   # must be in the redi/vagrant/ directory
   cd ./vagrant
   vagrant up
   </pre>

Vagrant will instantiate and provision the new VM. The REDCap web
application should be accessible in the browser at

http://localhost:8998/redcap/

If port 8998 is already in use vagrant will choose a different port
automatically. Read the log of "vagrant up" and note the port to be
used.

4. Verify the VM is running
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verify that the virtual machine is working properly by accessing it
using:

.. raw:: html

   <pre>
   vagrant ssh
   </pre>

5. Import Enrollment Data using RED-I
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Import the `sample subject
list <../config-example/vagrant-data/enrollment_test_data.csv>`__ into
REDCap by executing:

.. raw:: html

   <pre>
   make rc_enrollment
   </pre>

Note: This step is necessary because in order to associate data with
subjects the list of subjects needs to exist in the REDCap database.

6. Import Electronic Health Records using RED-I
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Import the `sample electronic health
records <../config-example/vagrant-data/redi_sample_project_v5.7.4.sql>`__
into REDCap by executing:

.. raw:: html

   <pre>
   make rc_post
   </pre>

Verify that the output of this command ends with:

.. raw:: html

   <pre>
   You can review the summary report by opening: report.html in your browser
   </pre>

If this step succeded you have verified that RED-I can be used to save
time by automating EHR data imports into REDCap.

Congratulations! You can now add your own REDCap project
and start using RED-I to move data.
Please refer to :doc:`add_new_redcap_project` document for help.
