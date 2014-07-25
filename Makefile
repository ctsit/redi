all: compile

build: compile
compile:
	python -m compileall bin
	python -m compileall test

test: tests
tests:
	python test/TestSuite.py

coverage:
	which figleaf || sudo easy_install figleaf
	figleaf test/TestSuite.py
	figleaf2html -d coverage .figleaf
	ls coverage/index.html

clean:
	rm -rf coverage
	rm -f .figleaf
	find . -type f -name *.pyc -print | xargs rm -f
