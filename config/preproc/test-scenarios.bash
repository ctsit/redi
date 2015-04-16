#!/bin/bash

function test_scenario
{
	SCENARIO=$1
	PREFIX=scenario${SCENARIO}
	cp ${PREFIX}/input.csv ../raw.txt
	mkdir testout/$PREFIX
	redi -c ../ -d -D testout/$PREFIX/outdir
	cp ../raw.txt testout/${PREFIX}/actual.csv
	diff -u ${PREFIX}/expected.csv testout/${PREFIX}/actual.csv
	echo ''
	echo Test passed.
	echo ''
	echo ''
}

set -e

rm -rf testout
mkdir testout

# Scenario 1: 0 tests before consent date
test_scenario 1
# Scenario 2: 1 test before consent date, 2 after
test_scenario 2
# Scenario 3: 2 tests before consent date
test_scenario 3
# Scenario 4: 4 tests before consent date
test_scenario 4
# Scenario 5: Multiple fields for same panel
test_scenario 5
