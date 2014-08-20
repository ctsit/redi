ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

all: build
build: egg
egg:
	python setup.py bdist_egg

install:
	easy_install dist/REDI*.egg

test: tests
tests: coverage
	[ ! -d config/rules ] || PYTHONPATH=bin \
		python -munittest discover config/rules

coverage:
	ARCHFLAGS=$(ARCHFLAGS) PYTHONPATH=bin \
		python setup.py nosetests

lint:
	which pylint || sudo easy_install pylint
	ARCHFLAGS=$(ARCHFLAGS) PYTHONPATH=bin \
		pylint -f parseable bin | tee pylint.out

clean:
	find . -type f -name "*.pyc" -print | xargs rm -f
	rm -rf out
	rm -rf dist
	rm -rf build
	rm -rf REDI.egg-info
	rm -rf nosetests.xml cover .coverage coverage.xml
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

