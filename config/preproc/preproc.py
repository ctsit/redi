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
import shutil


clinical_component_to_loinc_path = 'clinical-componenet-to-loinc-mapping.xml'
results_path = 'raw.txt'
subject_id_column = 'STUDY_ID'
translation_table_path = 'translationTable.xml'


def run_processing():
    rows = load(results_path)
    subject_ids = []
    for row in rows:
        subject_ids.append(row[subject_id_column])

    consent_dates = fetch_consent_dates(subject_ids)
    panels = fetch_panels('clinical-componenet-to-loinc.xml',
                          'translationTable.xml')
    # panels = {
    #     'rna': [1230, 3774, 1914, 4189, 6912, 1561675, 6860],
    #     'cbc': [1534435, 918, 1534444, 1577116, 1009, 1558101, 1539315, 913, 999, 1577876]
    #     'chem': [1534098, 971, 1534081, 968, 1810650, 1526000, 1525870, 1558221, 1534076]
    #     'inr': [1534098, 1810583]
    # }
    grouped_by_panel = group_rows_by_panel(panels, rows)
    # grouped_by_panel = {
    #     'rna': [<csv_row>, <csv_row>, <csv_row>],
    #     'cbc': [],
    #     'NONE': [<csv_row>, <csv_row>]
    # }
    filtered = filter_old_labs(grouped_by_panel, consent_dates)
    save(rows.fieldnames, filtered, results_path)


def fetch_consent_dates(subject_ids):
    raise NotImplementedError()


def fetch_panels(loinc_mapping, translation_table):
    raise NotImplementedError()


def filter_old_labs(rows, consent_dates):
    raise NotImplementedError()


def group_rows_by_panel(panels, rows):
    raise NotImplementedError()


def load(filepath):
    # with open(filepath) as fp:
    #     return csv.DictReader(fp)
    raise NotImplementedError()


def main():
    run_processing()


def save(headers, rows, path, backup=shutil.copy2, open_file=open):
    if backup:
        backup(path, path + '.bak')

    with open_file(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(iter(rows))


if __name__ == "__main__":
    main()