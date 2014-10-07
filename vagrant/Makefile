# This file is intended to help the developers
# with common testing tasks.
#
# Note: Some tasks depend on variables set in the config file
# therefore the proper path must be set for `CONFIG_FOLDER`
MAKE_CONFIG_FILE     := Makefile.ini

ifneq ("$(wildcard $(MAKE_CONFIG_FILE))", "")
   CONFIG_FOLDER        := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'config_folder=' | cut -d '=' -f2)
   CONFIG_FOLDER_VAGRANT:= $(CONFIG_FOLDER)/vagrant-data/
   CONFIG_FILE          := $(CONFIG_FOLDER)/settings.ini

   REDCAP_DB_SQL_FILE   := $(CONFIG_FOLDER_VAGRANT)/$(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_db_sql_file=' | cut -d '=' -f2)
   REDCAP_CODE_ZIP_FILE := $(CONFIG_FOLDER_VAGRANT)/redcap.zip
   REDCAP_SQL_PATCHES_FOLDER := $(CONFIG_FOLDER_VAGRANT)/sqlPatches
   ENROLLMENT_CSV_FILE  := $(CONFIG_FOLDER_VAGRANT)/enrollment_test_data.csv
   REFERENCE_OUTPUT_FILE:= $(CONFIG_FOLDER_VAGRANT)/redi_out_reference.csv

   REDCAP_API_URI := $(shell cat ${CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_uri=' | cut -d '=' -f2)
   REDCAP_VM_URI := $(subst api/,,$(REDCAP_API_URI))
   REDCAP_VM_TOKEN := $(shell cat ${CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'token=' | cut -d '=' -f2)
   REDCAP_RECORDS_CMD:=../bin/utils/redcap_records.py --token=$(REDCAP_VM_TOKEN) --url=$(REDCAP_API_URI)
   REDCAP_PROJECT_ID := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_project_id=' | cut -d '=' -f2)
   REDCAP_PROJECT_FORMS := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_project_forms=' | cut -d '=' -f2)
   REDCAP_PROJECT_ENROLLMENT_FORM := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_project_enrollment_form=' | cut -d '=' -f2)
endif

.PHONY: help
help:
	@echo "\n Available tasks:"
	@echo "\t copy_config_example - copy the required Makefile.ini from 'config-example' folder"
	@echo "\t copy_config_develop - copy the required Makefile.ini from developer's 'config' folder"
	@echo "\t show_config         - display the parameters retrieved from $(CONFIG_FILE)"
	@echo "\t copy_redcap_code:   - copy the redcap.zip file from the 'config' folder if available"
	@echo "\t copy_project_data:  - copy extra files from the 'config' folder if available"

	@echo "\t rc_check      - checks if REDCap is running"
	@echo "\t rc_list       - list the id of all REDCap projects"
	@echo "\t rc_save       - save a backup of REDCap database"
	@echo "\t rc_clean      - remove data for default test project"
	@echo "\t rc_enrollment - load csv enrollment test data for the default project"
	@echo "\t rc_get_enrollment - retrieve csv enrollment test data for the default project"
	@echo "\t rc_post       - send test data to REDCap"
	@echo "\t rc_get        - get stored test data from REDCap"
	@echo "\t rc_get_json   - get stored test data from REDCap in json format"
	@echo "\t rc_fresh      - erase/insert/retrieve test data from REDCap"
	@echo "\t rc_get_rate   - shows the config option value: 'page_hit_threshold_per_minute' "
	@echo "\t rc_set_rate   - set the value for: 'page_hit_threshold_per_minute' "

	@echo "\t egg_test      - deploy the redi egg file to the vagrant box and run redi"
	@echo "\t clean         - remove files created by testing"
	@echo "\t rc_compare    - compares the output data from REDCap to the reference dataset"

show_steps:
	@echo "\n Steps for importing data into the sample project:"
	@echo "\t make clean"
	@echo "\t make copy_config_example"
	@echo "\t make copy_redcap_code"
	@echo "\t make copy_project_data"
	@echo "\t make show_config"
	@echo "\t vagrant up"
	@echo "\t make rc_enrollment"
	@echo "\t make rc_post"
	@echo "\t make rc_get"

copy_config_example:
	@# Copy the config file for running make tasks
	cp ../config-example/vagrant-data/Makefile.ini .

copy_config_develop:
	cp ../config/vagrant-data/Makefile.ini .

check_config:
	@# This task is used as a dependency checker
	@test -f $(MAKE_CONFIG_FILE) || (echo 'Please obtain the required configuration file "Makefile.ini" by executing make task "copy_config_example" or "copy_config_develop"' && exit 1)
	@test -d $(CONFIG_FOLDER) || (echo 'Please create a "config" folder with necessary files first' && exit 1)
	@test -f $(CONFIG_FILE) || (echo 'Please obtain the config file "$(CONFIG_FILE)"' && exit 1)
	@test -f $(REDCAP_DB_SQL_FILE) || (echo 'Please obtain the project sql dump file "$(REDCAP_DB_SQL_FILE)"' && exit 1)
	@test -f $(REDCAP_CODE_ZIP_FILE) || (echo 'Please obtain the redcap software zip file "$(REDCAP_CODE_ZIP_FILE)"' && exit 1)
	@test -f $(ENROLLMENT_CSV_FILE) || (echo 'Config error: missing file "$(ENROLLMENT_CSV_FILE)"' && exit 1)

show_config: check_config
	@echo "$(MAKE_CONFIG_FILE) indicates that extra parameters should be read from : $(CONFIG_FILE)"
	@echo "Using REDCAP_DB_SQL_FILE : $(REDCAP_DB_SQL_FILE)"
	@echo "Using REDCAP_VM_URI : $(REDCAP_VM_URI)"
	@echo "Using REDCAP_VM_TOKEN : $(REDCAP_VM_TOKEN)"
	@echo "Using REDCAP_RECORDS_CMD : $(REDCAP_RECORDS_CMD)"
	@echo "Using REDCAP_PROJECT_ID : $(REDCAP_PROJECT_ID)"
	@echo "Using REDCAP_PROJECT_FORMS : $(REDCAP_PROJECT_FORMS)"
	@echo "Using REDCAP_PROJECT_ENROLLMENT_FORM : $(REDCAP_PROJECT_ENROLLMENT_FORM)"

copy_redcap_code: check_config
	cp $(REDCAP_CODE_ZIP_FILE) .

copy_project_data: check_config
	@# Bring in the REDCap database file with a name expected by bootstrap.sh
	cp $(REDCAP_DB_SQL_FILE) redcap_database.sql
	#@test ! -d $(REDCAP_SQL_PATCHES_FOLDER) || (echo "Copying 'sqlPatches' folder to vagrant folder" && cp -r $(REDCAP_SQL_PATCHES_FOLDER) .)

rc_check: check_config
	curl -s $(REDCAP_VM_URI) | grep -i  'Welcome\|Critical Error'

rc_list:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -l'

rc_save:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -b'

rc_clean:
	# TODO: add support for project id as parameter
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -d $(REDCAP_PROJECT_ID)'

rc_enrollment: check_config
	$(REDCAP_RECORDS_CMD) -i $(ENROLLMENT_CSV_FILE)

rc_post:
	python ../bin/redi.py -c $(CONFIG_FOLDER)

rc_get: check_config
	$(REDCAP_RECORDS_CMD) -f "$(REDCAP_PROJECT_FORMS)"

rc_get_json: check_config
	$(REDCAP_RECORDS_CMD) -f "$(REDCAP_PROJECT_FORMS)" -t json

rc_get_enrollment: check_config
	$(REDCAP_RECORDS_CMD) -f "$(REDCAP_PROJECT_ENROLLMENT_FORM)" -t csv

rc_fresh:
	make copy_project_data
	make rc_clean
	make rc_enrollment
	make rc_post
	make rc_get

rc_get_rate:
	vagrant ssh -c 'mysql -uroot -ppassword -e "select * FROM redcap.redcap_config WHERE field_name = \"page_hit_threshold_per_minute\" "'

rc_set_rate:
	# echo $(filter-out $@,$(MAKECMDGOALS))
	vagrant ssh -c 'mysql -uroot -ppassword -e "UPDATE redcap.redcap_config SET value = $(filter-out $@,$(MAKECMDGOALS)) WHERE field_name = \"page_hit_threshold_per_minute\" "'

rc_compare:
	@# This task can be used to compare the current project data with the reference data
	$(REDCAP_RECORDS_CMD) -f "$(REDCAP_PROJECT_FORMS)" > out.csv
	diff -u $(REFERENCE_OUTPUT_FILE) out.csv

test_egg:
	make egg_test

egg_test: check_config
	@test -f ../dist/REDI*.egg || (echo 'Please execute "make egg" from the project root first'			&& exit 1)
	cp ../dist/REDI*.egg .
	vagrant ssh -c 'sudo easy_install /vagrant/REDI*.egg'
	make rc_clean
	make rc_enrollment
	vagrant ssh -c 'redi -c /vagrant/config'

clean:
	@# This task removes all copied/generated files
	rm -f redcap.zip
	rm -f Makefile.ini
	rm -f projectDataBootstrap.sql
	rm -f out.csv
