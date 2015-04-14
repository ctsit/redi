#!/usr/bin/env python

# Contributors:
# Nicholas Rejack <nrejack@ufl.edu>
# Kevin Hanson <hansonks@gmail.com>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause
import csv
import os
import shutil
import StringIO

from redcap import Project, RedcapError
from utils import SimpleConfigParser
import redi as redi

SUBJECT_ID_COLUMN = 'study_id'
# REDCap field used to denote consent date
CONSENT_DATE_RC_FIELD = "eot_dsstdtc"
SUBJECT_ID_RC_FIELD = "consent_usubjid"

def run_processing(settings):
    translation_table_path = settings.translation_table_file
    component_to_loinc_path = settings.component_to_loinc_code_xml
    try:
        redcap_settings = redi.get_redcap_settings(settings)
    except Exception as ex:
        logger.error("Can't load REDCap settings: ", ex)

    results_path = os.path.realpath(
        os.path.join(__file__, '..', '..', 'synthetic-lab-data.csv'))

    rows = load(results_path)
    subject_ids = []
    for row in rows:
        subject_ids.append(row[SUBJECT_ID_COLUMN])

    consent_dates = fetch_consent_dates(subject_ids, redcap_settings)
    panels = fetch_panels(component_to_loinc_path, translation_table_path)

    grouped_by_panel = group_rows_by_panel(panels, rows)
    #grouped_by_panel = {
    #    'rna': [<csv_row>, <csv_row>, <csv_row>],
    #    'cbc': [],
    #    'NONE': [<csv_row>, <csv_row>]
    #}

    filtered = filter_old_labs(grouped_by_panel, consent_dates)
    save(rows.fieldnames, filtered, results_path)


def fetch_consent_dates(subject_ids, redcap_settings):
    """
    Fetch consent dates. 
    First, query for all consent date and subject IDs.
    Then match subject IDs in input set.
    """
    token = redcap_settings['token']
    url = redcap_settings['redcap_uri']
    verify_ssl = redcap_settings['verify_ssl']

    # we want the consent date, as well as the subject ID
    fields = CONSENT_DATE_RC_FIELD + "," + SUBJECT_ID_RC_FIELD

    try:
        project = Project(url, token, "", verify_ssl)
        source_subject_ids = project.export_records(
            fields=fields,
            events="1_arm_1")
        #logger.debug(str(source_subject_ids))
    except Exception as ex:
        print fields, source_subject_ids
        print "Cannot connect to project at " + url + ' with token ' + token
        quit()

   


def fetch_panels(loinc_mapping, translation_table):
    return {
        'rna': [1230, 3774, 1914, 4189, 6912, 1561675, 6860],
        'cbc': [1534435, 918, 1534444, 1577116, 1009, 1558101, 1539315, 913,
                999, 1577876],
        'chem': [1534098, 971, 1534081, 968, 1810650, 1526000, 1525870, 1558221,
                 1534076],
        'inr': [1534098, 1810583]
    }


def filter_old_labs(rows, consent_dates):
    raise NotImplementedError()


def group_rows_by_panel(panels, rows):
    raise NotImplementedError()


def load(filepath):
    with open(filepath) as fp:
        content = fp.read()
    return csv.DictReader(StringIO.StringIO(content))


def main():
    settings = SimpleConfigParser.SimpleConfigParser()
    config_file = os.path.realpath(os.path.join(__file__, '..', '..',
                                                'settings.ini'))
    settings.read(config_file)
    # this method reduces the syntax
    settings.set_attributes()
    run_processing(settings)


def save(headers, rows, path, backup=shutil.copy2, open_file=open):
    if backup:
        backup(path, path + '.bak')

    with open_file(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(iter(rows))


if __name__ == "__main__":
    main()