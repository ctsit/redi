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
	@echo "\t pypi             - upload files to https://pypi.python.org/pypi/redi-py"
	@echo "\t show_pips        - show python packages installed globally"
	@echo "\t venv_help        - show commands for installing 'redi-py' package in the 'venv' virtual environment"
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
	rm -rf out dist build
	rm -rf *.egg-info
	rm -rf nosetests.xml cover .coverage coverage.xml
	rm -f unittest_pysftp_rsa_key unittest_pysftp_rsa_key.pub destination_file source_file
	rm -rf *.egg
	rm -f pylint.out
	rm -f formData.xml
	rm -f rawData.xml
	rm -f translationalData.xml
	rm -f rawDataWithFormName.xml
	rm -f rawDataWithFormCompletedField.xml
	rm -f rawDataWithDatumAndUnitsFieldNames.xml
	rm -f rawDataSorted.xml
	rm -f rawDataWithAllUpdates.xml
	rm -f rawDataWithFormImported.xml
	rm -f rawDataWithFormStatus.xml
	rm -f all_form_events.xml
	rm -f person_form_event_tree.xml
	rm -f person_form_event_tree_with_data.xml
	rm -rf vagrant/data/
	rm -f vagrant/redi.db
	rm -f config-example/report.xml
	rm -f redi.pstats

pypi:
	#https://pythonhosted.org/Distutils2/distutils/packageindex.html
	python setup.py sdist register upload -r pypi

show_pips:
	find /Library/Python/2.7/site-packages/ -maxdepth 2 -name __init__.py | cut -d '/' -f 6

venv_help:
	@echo "\n To install 'redi' in the virtual environment please execute: \n\n\t virtualenv venv && source venv/bin/activate && pip install redi-py"
	@echo "\n To destroy the virtual environment please execute: \n\n\t deactivate && rm -rf ./venv"

venv_show_pips:
	find venv/lib/python2.7/site-packages/ -maxdepth 2 -name __init__.py | cut -d '/' -f5
