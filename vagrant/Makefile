
DB_FILE=$(shell python -c 'from appdirs import AppDirs; dirs = AppDirs("redi"); print ("\"" + dirs.user_data_dir + "/0.10.0/redi.db\"")')

# Displays the list of available actions
help:
	@echo "\n Available tasks:"
	@echo "\t rc_check      - checks if REDCap is running"
	@echo "\t rc_save       - save a backup of REDCap database"
	@echo "\t rc_clean      - remove data for default test project"
	@echo "\t rc_clean_hcv  - truncates the extra 'hcv' tables such as: _hcvt2_ae, ..."
	@echo "\t rc_clean_who  - truncates the extra 'who' tables such as: _whodrug_atc, ..."
	@echo "\t rc_post       - send test data to REDCap"
	@echo "\t rc_get        - get stored test data from REDCap"
	@echo "\t rc_fresh      - erase/insert/retrieve test data from REDCap"
	@echo "\t rc_get_rate   - shows the config option value: 'page_hit_threshold_per_minute' "
	@echo "\t rc_set_rate   - set the value for: 'page_hit_threshold_per_minute' "
	@echo "\t egg_test      - deploy the redi egg file to the vagrant box and run redi"

	@echo "\t db_tables     : list the tables in the database"
	@echo "\t db_schema     : show the columns in the RediBatch table"
	@echo "\t db_list       : list the redi batches that have been run"
	@echo "\t db_last       : show the row corresponding to the last redi batch run"
	@echo "\t db_add        : insert sample row in the RediBatch table"
	@echo "\t db_fresh      : create a fresh database file"
	@echo "\t db_clean      : remove all rows from the RediBatch table"



rc_check:
	curl -s http://localhost:8998/redcap/ | grep -i  'Welcome\|Critical Error'

rc_list:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -l | grep example_proj_id_12'

rc_save:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -b'

rc_clean:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -d 12'


rc_demographics:
	../bin/utils/redcap_records.py --token=121212 --url=http://localhost:8998/redcap/api/ -i demographic_test_data.csv

rc_post:
	python ../bin/redi.py

rc_get:
	../bin/utils/redcap_records.py --token=121212 --url=http://localhost:8998/redcap/api/ -f "demgraphics chemistry"

rc_fresh:
	make rc_clean
	make rc_demographics
	make rc_post
	make rc_get

rc_get_rate:
	vagrant ssh -c 'mysql -uroot -ppassword -e "select * FROM redcap.redcap_config WHERE field_name = \"page_hit_threshold_per_minute\" "'

rc_set_rate:
	# echo $(filter-out $@,$(MAKECMDGOALS))
	vagrant ssh -c 'mysql -uroot -ppassword -e "UPDATE redcap.redcap_config SET value = $(filter-out $@,$(MAKECMDGOALS)) WHERE field_name = \"page_hit_threshold_per_minute\" "'

test_egg:
	make egg_test

egg_test:
	@test -f ../dist/REDI*.egg || (echo 'Please execute "make egg" from the project root first'			&& exit 1)
	@test -d config				|| (echo 'Please create a "config" folder with necessary files first'	&& exit 1)
	cp ../dist/REDI*.egg .
	vagrant ssh -c 'sudo easy_install /vagrant/REDI*.egg'
	make rc_clean
	make rc_demographics
	vagrant ssh -c 'redi -c /vagrant/config'



get_extras:
	@test -d ../config    || (echo 'Please create a "config" folder with necessary files first'	&& exit 1)
	@test -f ../config/vagrant-data/redcap.zip || (echo 'Please obtain the redcap software zip file  first'	&& exit 1)
	@test -f ../config/vagrant-data/projectDataBootstrap.sql || (echo 'Please obtain the project sql dump first'	&& exit 1)
	cp -i ../config/vagrant-data/redcap.zip .
	cp -i ../config/vagrant-data/projectDataBootstrap.sql .

clean:
	rm -f report.html

db_tables:
	@echo "The database file $(DB_FILE) contains the following tables:"
	@sqlite3 $(DB_FILE) .tables

db_schema:
	@sqlite3 $(DB_FILE) 'PRAGMA table_info("RediBatch")'

db_list:
	@sqlite3 $(DB_FILE) "SELECT * FROM RediBatch"

db_last:
	@sqlite3 $(DB_FILE) "SELECT * FROM RediBatch ORDER BY rbID DESC LIMIT 1"

db_add:
	@sqlite3 $(DB_FILE) "INSERT INTO RediBatch (rbStartTime, rbStatus, rbMd5Sum) VALUES ( datetime('now'), 'Started', 'xyz');"

db_fresh:
	@rm -f $(DB_FILE)
	@touch $(DB_FILE)
	@sqlite3 $(DB_FILE) 'CREATE TABLE RediBatch ( rbID INTEGER PRIMARY KEY AUTOINCREMENT, rbStartTime TEXT NOT NULL, rbEndTime TEXT, rbStatus TEXT, rbMd5Sum TEXT NOT NULL);'
	@test -s redi.db || echo 'File redi.db was not created'

db_clean:
	@sqlite3 $(DB_FILE) "DELETE FROM RediBatch"
