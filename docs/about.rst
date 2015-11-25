RED-I Project
=============

.. figure:: https://zenodo.org/badge/doi/10.5281/zenodo.10014.png
   :alt: .

Introduction
------------

The REDCap Electronic Data Importer (RED-I) is a tool which is used to
automate the process of loading clinical data from Electronic Medical
Records (EMR) systems into `REDCap <http://www.project-redcap.org/>`__
Study data capture systems. RED-I is a general purpose tool for REDCap
data importing suitable for use on any study in any REDCap system. It
uses XML lookups to translate data stored in comma separated values
(CSV) files and uploads it to a REDCAP Server using the REDCap API. The
tool allows study data to be securely uploaded from clinical reporting
systems, error checked, and uploaded into REDCap. It provides the
investigator with feedback on upload success in the form of summary
reporting of the data upload process.

You can view a presentation of the RED-I tool in action on
`youtube <https://www.youtube.com/watch?v=0x04y5SNPL8&feature=youtu.be>`__.

How to Install RED-I
--------------------

RED-I is written in Python so you will have to install it if the
following comand gives you an error:

.. raw:: html

   <pre>
   $ python --version
   Python 2.7.5
   </pre>

For more details on how to install python on your system please visit
`Downloading
Python <https://wiki.python.org/moin/BeginnersGuide/Download>`__ page.

Installation Using Source Code
------------------------------------

We recommend to install RED-I in a Python virtual environment in order
to prevent conflicts with your other packages.

.. raw:: html

   <pre>
      $ wget https://bootstrap.pypa.io/get-pip.py
      $ python get-pip.py
   </pre>

The follow steps assume that you have the
`git <http://git-scm.com/book/en/Getting-Started-Installing-Git>`__
version control installed on your system.

.. raw:: html

   <pre>
      $ git clone https://github.com/ctsit/redi.git redi
      $ cd redi
      $ sudo pip install virtualenv
      $ virtualenv venv
      $ source venv/bin/activate
      $ make && make install
   </pre>

Once you are done with testing RED-I and you are satisfied with the
results you can remove the virtualenv artifacts and install the RED-I
package to be available system-wide.

.. raw:: html

   <pre>
      $ deactivate
      $ rm -rf venv/
      $ make && make install
   </pre>

Please refer to :doc:`redi_installation` document for more help
with the installation.

Installation Using Binary Distribution
--------------------------------------------

.. raw:: html

   <pre>
      $ pip install redi
   </pre>

To uninstall the application:

.. raw:: html

   <pre>
      $ pip uninstall redi
   </pre>

.. seealso:: http://pip.readthedocs.org/en/latest/reference/pip.html

Installing RED-I on Windows
----------------------------

* Open a command prompt by clicking on the Start menu, and typing "cmd" in the Run box.
* Install 64-bit Python 2.7.9 by running the following command in the command prompt:

.. raw:: html
   
   <pre>
      msiexec /i https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi 
   </pre>

* Next you need to be insure the command interpreter will be able to find the Python modules. Set
the paths to the modules by running the following commands in the command prompt:

.. raw:: html
   
   <pre>
      setx path "%path%;c:\python27"
      setx path "%path%;c:\python27\lib\site-packages"
      setx path "%path%;c:\python27\scripts”
   </pre>

* Make a new directory for the RED-I files by running the following command in the command prompt:

.. raw:: html
   
   <pre>
      mkdir c:\redi
   </pre>

* Download the RED-I source code from: [https://github.com/ctsit/redi/archive/0.14.1.zip]
* Copy the contents of the RED-I zip file from c:\Users\%username%\Downloads\redi-0.14.1\redi-0.14.1 to c:\redi
* Download the easy_install setup file from: https://bootstrap.pypa.io/ez_setup.py 
* Run the easy_install setup file with the following command in the command prompt:

.. raw:: html
   
   <pre>
      python c:\Users\%username%\Downloads\ez_setup.py
   </pre>

Note: you may need to modify the path to the ez_setup.py file if it is downloaded to a different location.

* Next, make a binary install of RED-I by running the following commands in the command prompt:

.. raw:: html
   
   <pre>
      cd c:\redi
      python c:\redi\setup.py bdist_egg
   </pre>

* You will need to manually install the pycrypto dependency. To avoid having to compile it with VCForPython you can
download a pre-compiled binary and install it with the following command:

.. raw:: html

   <pre>
      c:\python27\scripts\easy_install http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win-amd64-py2.7.exe
   </pre>

* Finally, install your binary of RED-I with the following command:

.. raw:: html
   
   <pre>
      c:\python27\scripts\easy_install.exe c:\redi\dist\redi-0.14.1-py2.7.egg
   </pre>

Installing RED-I on Red Hat and Fedora
----------------------------
Download and install setuptools. Setuptools will aid you in installing the redi package. 

.. raw:: html

   <pre>
   curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && sudo python get-pip.py
   </pre>

Note that you must have gcc (the Gnu Compiler Collection) to build RED-I. Check that you have gcc installed:

.. raw:: html

   <pre>
   gcc --version
   </pre>

If gcc is not installed, install it:

.. raw:: html

   <pre>
   sudo yum install gcc
   </pre>

Install the development libxslt, libxml2, and python-devel libraries. These allow you to build the redi source.

.. raw:: html

   <pre>
   sudo yum install libxslt-devel libxml2-devel python-devel
   </pre>

Install redi using pip.

.. raw:: html

   <pre>
   sudo pip install redi
   </pre>

RED-I is now be installed. 

If you get an error message while compiling pycrypto, you will need to install pycrypto separately:

.. raw:: html

   <pre>
   sudo yum install python-crypto
   </pre>

* To use the example config, documentation, and other associated RED-I files, you will need to get files from the GitHub repository. You have two options: 

1.  Clone the repo by using Git.

.. raw:: html

   <pre>
   yum install git
   </pre>

Set up your install of Git to use the key on your GitHub account. Instructions are at: https://help.github.com/articles/generating-ssh-keys/

Now, clone the redi git repo:

.. raw:: html

   <pre>
   clone git@github.com:ctsit/redi.git
   </pre>

You now have a directory called redi with the source, docs, example configuration and other RED-I files.

2.  Download the zip file

.. raw:: html

   <pre>
   wget https://github.com/ctsit/redi/archive/master.zip
   sudo yum install unzip
   unzip master.zip
   </pre>

* You now have a directory called redi-master with the source, docs, example configuration and other RED-I files.

How to Test RED-I with a Sample Project
---------------------------------------

Now that you installed the RED-I application you are probably wondering
how to configure it to help you with data translation and import tasks.
The good news is that you do not have to change any configuration file
to test RED-I -- we provide examples of working files for you:

-  :download:`Vagrantfile <../vagrant/Vagrantfile>`
      --> allows to run a local REDCap instance
-  :download:`settings.ini <../config-example/settings.ini>`
      --> pre-configures RED-I to send data to the local REDCap instance
-  :download:`Makefile.ini <../config-example/vagrant-data/Makefile.ini>`
      --> configures the `make <http://www.gnu.org/software/make/manual/>`__
      tasks from :download:`Makefile <../vagrant/Makefile>` to simplify testing
-  :download:`redi\_sample\_project\_v5.7.4.sql <../config-example/vagrant-data/redi_sample_project_v5.7.4.sql>`
      --> provides the data for the sample project running in the local
      REDCap instance

These files make it very easy to see how RED-I imports data from a `csv
file <config-example/synthetic-lab-data.csv>`__ into a local instance of
REDCap. You just have to follow the instructions from the
:doc:`test_sample_project_using_vagrant` document.

**Note:** You will need to obtain your own copy of the REDCap since `the
license terms <https://redcap.vanderbilt.edu/consortium/participate.php>`__
prevent us from including the code in an open source project.

How to Configure RED-I for a New Project
----------------------------------------

To use RED-I in production you will have to edit the 'settings.ini' file
with values matching your environment.

Please refer to the :doc:`redi_configuration` for
more details about the meaning of each parameter in 'settings.ini' file.

Please refer to the :doc:`add_new_redcap_project` document for more details
about new project setup.

One of the advantages of using RED-I is that it allows to be customized
in order to send data to multiple types forms in REDCap projects. Please
refer to :doc:`describing_a_redcap_form_to_redi` document for more
details on how to create two of the required configuration files.

How to use RED-I
----------------

.. raw:: html

   <pre style="padding: 1em; background: #000; color: #0f0; font: normal 1em Courier, Andale Mono">
   $ redi -c config-example
   </pre>

Please refer to the :doc:`redi_usage` for more
details about all arguments supported in the command line.

How to Get Support
------------------

If you need any help with using RED-I please email us at ctsit@ctsi.ufl.edu

How to Contribute
-----------------

-  Fork the source-code
-  Create a branch (:command:`git checkout -b my_branch`)
-  Commit your changes
   (:command:`git commit -am "Details about feature/bug fixes in the commit"`)
-  Push to the branch (:command:`git push origin my_branch`)
-  Open a pull request and we will accept it as long as it conforms to our
:doc:`code_review_checklist`

