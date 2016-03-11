Regression Testing
==================

The intent of the procedure described below is to find new bugs or
unexpected side effects in the code after a release lifecycle is
completed.

``Goal``: Compare two files obtained from RedCAP after two separate
imports are performed using the production and the candidate versions of
REDI software.

Note: The login credentials for the RedCAP web application on the
testing VM at http://localhost:8998/redcap/index.php are:
``admin/password``

Steps
-----

1. Obtain the candidate version (redi\_B) of the software

   ::

       $ git clone git@repo_redi redi_new
       $ cd redi_new && git checkout develop

-  Clone the config repository at ./config and checkout the tag that
   matched the REDI version

   git clone git@repo\_config config cd config && git checkout develop

-  If needed, revise the settings.ini lines that identify the host and
   authorize access. For this VM, the lines are

   ::

       "redcap_uri": "http://localhost:8998/redcap/api/",
       "token": "121212",

       $ sed -i 's/^\s\+"redcap_uri.*/\t"redcap_uri" : "http:\/\/localhost:8998\/redcap\/api\/",/' settings.ini
       $ sed -i 's/^\s\+"token.*/\t"token" : "121212",/' settings.ini

-  Go to the vagrant folder and remove the old virtual machine (VM)
   instance if necessary:

   ::

        $ cd vagrant && vagrant destroy

-  Start a fresh VM:

   $ vagrant up

The expected output from this command should look like:

::

         redcap.zip content indicates Redcap version: 5.7.4
         Setting the connection variables in: /var/www/redcap/database.php
         Checking if redcap application is running...
            <b>Welcome to REDCap!</b>

-  If you need to preserve the database state then you can create a
   backup of the REDCap database before we insert any data by running
   the redcapdbm.php script on the VM:

   $ vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -b'

Note: The commands above create a file like
``backup-redcap-YYYYmmdd-HHMM.sql`` on the VM

-  Erase the data in the REDCap instance using redcapdbm.php. First,
   enumerate the REDCap projects

   $ vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -l'

   The following projects are currently available in the redcap
   database:

   project\_id: 1, project\_name: redcap\_demo\_cda700 project\_id: 2,
   project\_name: redcap\_demo\_f3746b project\_id: 3, project\_name:
   redcap\_demo\_117155 ... project\_id: 12, project\_name:
   hcvtarget\_20\_development ...

Erase the data in the correct project if necessary:

::

      $ cd ../vagrant && vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -d 12'

       Deleting data for project: 12, name: hcvtarget_20_development
       Rows deleted from `redcap_surveys_response`:0
       Rows deleted from `redcap_surveys_participants`:0
       Rows deleted from `redcap_surveys_emails`:0

-  If needed, load a minimal set of data to get research identifiers
   into REDCap. Use the redcap\_records utility to load this data.

   ::

        $ redcap_records --token=121212 --url=http://localhost:8998/redcap/api/ -i demographic_test_data.csv

On success the following text is returned:

``{u'count': 5}``

-  Upload raw.txt file to REDCap using redi\_B

   Note: You may want to increase the number of requests allowed for
   processing before proceeding with data upload.

   ::

       Open the address "localhost:8998" using your browser

       Login to REDCap and then click on "Control Center" tab

       Click on the "Security & Authentication Configuration" link on the left menu

       Find and adjust the "Rate Limiter" field to something like 60000


       $ python ../redi/redi.py

If the output from the command above produces an exception then check if
your IP was not banned due to numerous requests sent (@see related code
in Config/init\_functions.php: ``checkBannedIp() and storeHashedIp()``)

::

         select * from redcap_ip_banned where ip = '10.0.2.2';
         +----------+---------------------+
         | ip       | time_of_ban         |
         +----------+---------------------+
         | 10.0.2.2 | 2014-06-06 18:59:25 |
         +----------+---------------------+

To fix this, use these SQL commands:

::

      update redcap_config set value = 600000 where field_name = 'page_hit_threshold_per_minute';
      delete from redcap_ip_banned;

If the token is invalid the following error is returned:

``Cannot connect to project at http://localhost:8998/redcap/api/ with token 121212``

-  Download relevant forms from REDCap using a command like:

   ::

        $ redcap_records --token=121212 --url=http://localhost:8998/redcap/api/ -f "demgraphics chemistry" > output_B.csv

If you have a lot of forms, the output comparison is easier if you
export the forms separately like this:

::

        #!/bin/bash

        batch=$1
        forms="demographics chemistry cbc inr hcv_rna_results"
        if [ ! -e $batch ]; then
            mkdir $batch
        fi

        for form in $forms
            do
              redcap_records --token=121212 --url=http://localhost:8998/redcap/api/ --forms=$form > $batch/$form.csv
            done

Later do the diff like this:

::

        diff -ur a/ b/

-  At this point we have gathered the output from the release candidate
   software redi\_B. If we there is reference output file available than
   we can just compare the outputs:

   ::

       $ diff -u output_A.csv output_B.csv

-  If there is no reference output file available than we have to get a
   previous version redi\_A and generate it.

   Erase the REDCap data first:

   ::

       cd ../vagrant && vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -d 12'

-  Obtain the reference version (redi\_A) of redi software.

   ::

       $ git clone git@repo_redi redi_old
       $ cd redi_old && git checkout TAG_ID_OLD

       $ git clone git@repo_config config
       $ cd ../config && git checkout TAG_ID_OLD_CONFIG

-  Repeat steps 8-10 with redi\_A software with the only difference
   being that the output file is changed to ``output_A.csv`` on step 10.

-  Compare the files ``output_A.csv`` and ``output_B.csv`` to insure
   there are no differences or expected differences are present:

   ::

       $ diff -u output_A.csv output_B.csv

If no new behavior was introduced the output from the command above
should be an empty string.
