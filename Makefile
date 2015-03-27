ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

all: build
build: egg
egg:
	python setup.py bdist_egg

install:
	easy_install dist/redi*.egg

help:
	@echo "Available tasks :"
	@echo "\t build            - generate the dist/*.egg file"
	@echo "\t install          - run the installation of the dist/*.egg file"
	@echo "\t test             - rin all unit tests"
	@echo "\t coverage         - run code coverage analysis"
	@echo "\t lint             - check code for sytax error"
	@echo "\t clean            - remove generated files"
	@echo "\t pypi             - upload files to https://pypi.python.org/pypi/redi"
	@echo "\t show_pips        - show python packages installed globally"
	@echo "\t venv_help        - show commands for installing 'redi' package in the 'venv' virtual environment"
	@echo "\t venv_show_pips   - show python packages installed in the 'venv' virtual environment"

test: tests
tests: coverage
	[ ! -d config/rules ] || python -munittest discover config/rules
	rm -f .coverage
	rm -rf cover/
	rm -f coverage.xml nosetests.xml

coverage:
	ARCHFLAGS=$(ARCHFLAGS) python setup.py nosetests

lint:
	which pylint || sudo easy_install pylint
	ARCHFLAGS=$(ARCHFLAGS) pylint -f parseable redi | tee pylint.out

clean:
	find . -type f -name "*.pyc" -print | xargs rm -f
	@rm -rf out dist build *.egg-info *.egg
	@rm -rf nosetests.xml cover .coverage coverage.xml
	@rm -f pylint.out unittest_pysftp_rsa_key unittest_pysftp_rsa_key.pub destination_file source_file
	@rm -f formData.xml rawData.xml translationalData.xml rawDataWithFormName.xml rawDataWithFormCompletedField.xml
	@rm -f rawDataWithDatumAndUnitsFieldNames.xml rawDataSorted.xml rawDataWithAllUpdates.xml rawDataWithFormImported.xml rawDataWithFormStatus.xml
	@rm -f all_form_events.xml person_form_event_tree.xml person_form_event_tree_with_data.xml
	@rm -f vagrant/redi.db config-example/report.xml redi.pstats mprofile_*.dat

pypi:
	#https://pythonhosted.org/Distutils2/distutils/packageindex.html
	python setup.py sdist register upload -r pypi

show_pips:
	find /Library/Python/2.7/site-packages/ -maxdepth 2 -name __init__.py | cut -d '/' -f 6

venv_help:
	@echo "\n To install 'redi' in the virtual environment please execute: \n\n\t virtualenv venv && source venv/bin/activate && pip install redi"
	@echo "\n To destroy the virtual environment please execute: \n\n\t deactivate && rm -rf ./venv"

venv_show_pips:
	find venv/lib/python2.7/site-packages/ -maxdepth 2 -name __init__.py | cut -d '/' -f5
