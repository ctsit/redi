all: compile

build: compile

egg:
	python setup.py bdist_egg

egg-test: egg
	bash scripts/egg-test.bash

bdist:
	python setup.py bdist

sdist:
	python setup.py sdist
compile:
	python -m compileall bin
	python -m compileall test

test: tests
tests:
	PYTHONPATH=bin python setup.py test
	[ ! -d config/rules ] || PYTHONPATH=bin python -munittest discover config/rules

coverage:
	which figleaf || sudo easy_install figleaf
	figleaf test/TestSuite.py
	figleaf2html -d coverage .figleaf
	ls coverage/index.html

clean:
	rm -rf coverage
	rm -f .figleaf
	find . -type f -name *.pyc -print | xargs rm -f
	rm -rf out/*
	rm -rf dist
	rm -rf build
	rm -rf REDI.egg-info
