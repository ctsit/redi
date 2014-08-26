# Displays the list of available actions
help:
	@echo "\n Available tasks:"
	@echo "\t rc_check      - checks if REDCap is running"
	@echo "\t rc_list       - list the id of all REDCap projects"
	@echo "\t rc_save       - save a backup of REDCap database"
	@echo "\t rc_clean      - remove data for default test project"
	@echo "\t rc_post       - send test data to REDCap"
	@echo "\t rc_get        - get stored test data from REDCap"
	@echo "\t rc_fresh      - erase/insert/retrieve test data from REDCap"
	@echo "\t rc_get_rate   - shows the config option value: 'page_hit_threshold_per_minute' "
	@echo "\t rc_set_rate   - set the value for: 'page_hit_threshold_per_minute' "
	@echo "\t egg_test      - deploy the redi egg file to the vagrant box and run redi"
	@echo "\t copy_redcap_code: - copy the redcap.zip file from the 'config' folder if available"
	@echo "\t copy_project_data: - copy *.sql files from the 'config' folder if available"
	

rc_check:
	curl -s http://localhost:8998/redcap/ | grep -i  'Welcome\|Critical Error' 

rc_list:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -l'

rc_save:
	vagrant ssh -c 'cd /vagrant/scripts && php redcapdbm.php -b'

rc_clean:
	# TODO: add support for project id as parameter
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

clean:
	rm -f report.html

copy_redcap_code:
	@test -d ../config    || (echo 'Please create a "config" folder with necessary files first'     && exit 1)
	@test -f ../config/vagrant-data/redcap.zip || (echo 'Please obtain the redcap software zip file first' && exit 1)
	cp -i ../config/vagrant-data/redcap.zip .

copy_project_data:
	@test -d ../config    || (echo 'Please create a "config" folder with necessary files first'     && exit 1)
	@test -f ../config/vagrant-data/projectDataBootstrap.sql || (echo 'Please obtain the project sql dump first' && exit 1)
	cp ../config/vagrant-data/projectDataBootstrap.sql .
	@test -f ../config/vagrant-data/demographic_test_data.csv || (echo 'Please obtain the demographics file first' && exit 1)
	cp ../config/vagrant-data/demographic_test_data.csv .
	test ! -d ../config/vagrant-data/sqlPatches || (echo "Copying sqlPatches folder from project configuration to vagrant folder" && cp -r ../config/vagrant-data/sqlPatches .)
