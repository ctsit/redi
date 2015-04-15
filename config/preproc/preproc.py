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
import datetime
import itertools
import os
import shutil
import StringIO

from redcap import Project, RedcapError

import redi
try:
    from redi.utils import SimpleConfigParser
except ImportError:
    from utils import SimpleConfigParser


SUBJECT_ID_COLUMN = 'study_id'
COMPONENT_ID_COLUMN = 'loinc_code'
TAKEN_TIME_COLUMN = 'date_time_stamp'
# REDCap field used to denote consent date
CONSENT_DATE_RC_FIELD = "consent_dssstdtc"
SUBJECT_ID_RC_FIELD = "dm_usubjid"

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
    fields = [CONSENT_DATE_RC_FIELD, SUBJECT_ID_RC_FIELD]
    events = ["1_arm_1"]

    try:
        project = Project(url, token, "", verify_ssl)
        source_subject_ids = project.export_records(
            events=events,
            fields=fields,
            forms="demographics")
    except Exception as ex:
        logger.error("Cannot connect to project at " + url + ' with token ' + token)
        quit()

    # make the list of subject_ids unique (convert to set)
    subject_ids = list(set(subject_ids))

    # process the source_subject_ids and passed in subject_ids
    # output a list that has the subject_ids and consent date
    # key is subject_id, value is consent date
    joined_subject_ids_and_consent_date = {}
    for row in subject_ids:
        for rc_row in source_subject_ids:
            if rc_row[SUBJECT_ID_RC_FIELD] == row:
                joined_subject_ids_and_consent_date[row] = rc_row[CONSENT_DATE_RC_FIELD]

    return joined_subject_ids_and_consent_date


def fetch_panels(loinc_mapping, translation_table):
    return {
        'rna': [1230, 3774, 1914, 4189, 6912, 1561675, 6860],
        'cbc': [1534435, 918, 1534444, 1577116, 1009, 1558101, 1539315, 913,
                999, 1577876],
        'chem': [1534098, 971, 1534081, 968, 1810650, 1526000, 1525870, 1558221,
                 1534076],
        'inr': [1534098, 1810583]
    }


def filter_old_labs(rows_grouped_by_panel, consent_dates):
    filtered = []

    def parse_date(date_string):
        DATE_FORMAT = '%Y-%m-%d'
        return datetime.datetime.strptime(date_string, DATE_FORMAT)

    def consent_date(row):
        subject_id = row[SUBJECT_ID_COLUMN]
        return parse_date(consent_dates[subject_id])

    for panel, rows in rows_grouped_by_panel.iteritems():
        after_consent = itertools.ifilter(
            lambda r: parse_date(r[TAKEN_TIME_COLUMN]) >= consent_date(r),
            rows)

        filtered += after_consent

        before_consent = itertools.ifilter(
            lambda r: parse_date(r[TAKEN_TIME_COLUMN]) < consent_date(r),
            rows)

        filtered += sorted(before_consent,
                           key=lambda r: parse_date(r[TAKEN_TIME_COLUMN]),
                           reverse=True)[:2]

    return filtered


def group_rows_by_panel(panels, rows):
    NO_PANEL = 'NONE'
    rows_by_panel = {name: [] for name in panels.iterkeys()}
    rows_by_panel[NO_PANEL] = []

    for row in rows:
        panel_name = next((name
                           for name, ids in panels.iteritems()
                           if row[COMPONENT_ID_COLUMN] in ids),
                          NO_PANEL)
        rows_by_panel[panel_name].append(row)

    return rows_by_panel


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