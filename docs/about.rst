RED-I Project
=============

.. figure:: https://zenodo.org/badge/doi/10.5281/zenodo.10014.png
   :alt: .

.. CONTENTS OF THIS FILE
.. ---------------------
.. 
.. -  `Introduction <#introduction>`__
.. -  `How to Install RED-I <#how-to-install-red-i>`__
.. -  `How to Test RED-I with a Sample
..    Project <#how-to-test-red-i-with-a-sample-project>`__
.. -  `How to Configure RED-I for a New
..    Project <#how-to-configure-red-i-for-a-new-project>`__
.. -  `How to Use RED-I <#how-to-use-red-i>`__
.. -  `How to Get Support <#how-to-get-support>`__
.. -  `How to Contribute <#how-to-contribute>`__

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

You can view a presentation of RED-I tool in action on
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

Installation Steps Using Source Code
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

Once you are done with testing RED-I an you are satisfied with the
results you can remove the virtualenv artifacts and install the RED-I
package to be available system-wide.

.. raw:: html

   <pre>
      $ deactivate
      $ rm -rf venv/
      $ make && make install
   </pre>

Please refer to `README-install <redi_installation.md>`__ for more help
with installation.

Installation Steps Using Binary Distribution
--------------------------------------------

@TODO

How to Test RED-I with a Sample Project
---------------------------------------

Now that you installed the RED-I application you are probably wondering
how to configure it to help you with data translation and import tasks.
The good news is that you do not have to change any configuration file
to test RED-I -- we provide examples of working files for you:

-  `Vagrantfile <vagrant/Vagrantfile>`__ - allows to run a local REDCap
   instance
-  `settings.ini <config-example/settings.ini>`__ - pre-configures RED-I
   to send data to the local REDCap instance
-  `Makefile.ini <config-example/vagrant-data/Makefile.ini>`__ -
   configures the `make <http://www.gnu.org/software/make/manual/>`__
   tasks from `Makefile <vagrant/Makefile>`__ to simplify testing
-  `redi\_sample\_project\_v5.7.4.sql <config-example/vagrant-data/redi_sample_project_v5.7.4.sql>`__
   - provides the data for the sample project running in the local
   REDCap instance

These files make it very easy to see how RED-I imports data from a `csv
file <config-example/synthetic-lab-data.csv>`__ into a local instance of
REDCap. You just have to follow the instructions from the `Testing RED-I
with a sample REDCap Project <../vagrant/README.md>`__.

**Note:** You will need to obtain your own copy of the REDCap since `the
license
terms <https://redcap.vanderbilt.edu/consortium/participate.php>`__
prevent us from including the code in an open source project.

How to Configure RED-I for a New Project
----------------------------------------

To use RED-I in production you will have to edit the 'settings.ini' file
with values matching your environment.

Please refer to the `RED-I Configuration <redi_configuration.md>`__ for
more details about the meaning of each parameter in 'settings.ini' file.

Please refer to the `Add new REDCap Project and API
Key <add_new_redcap_project.md>`__ document for more details about new
project setup.

One of the advantages of using RED-I is that it allows to be customized
in order to send data to multiple types forms in REDCap projects. Please
refer to `Describing a REDCap Form to
RED-I <describing_a_redcap_form_to_red-i.md>`__ document for more
details on how to create two of the required configuration files.

How to use RED-I
----------------

.. raw:: html

   <pre style="background: #000; color: #0f0; font: normal 1em Courier, Andale Mono">
   $ redi -c config-example
   </pre>

Please refer to the `advanced usage guide <redi_usage.md>`__ for more
details about all arguments supported in the command line.

How to Get Support
------------------

If you need any help with using RED-I please email us at \|CTS-IT-ALL\|
at \|ctsi.ufl.edu\|

How to Contribute
-----------------

-  Fork the source-code
-  Create a branch (``git checkout -b my_branch``)
-  Commit your changes
   (``git commit -am "Details about feature/bug fixes in the commit"``)
-  Push to the branch (``git push origin my_branch``)
-  Open a pull request and we will accept it as long as it passes
   through our `code review procedure <code-review-checklist.md>`__

