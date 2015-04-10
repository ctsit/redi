#!/usr/bin/env python

# Contributors:
# Nicholas Rejack <nrejack@ufl.edu>
# Kevin Hanson <hansonks@gmail.com>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

clinical_component_to_loinc_path = 'clinical-componenet-to-loinc-mapping.xml'
results_path = 'raw.txt'
subject_id_column = 'STUDY_ID'
translation_table_path = 'translationTable.xml'


def run_processing():
    backup(results_path)
    rows = load(results_path)
    subject_ids = []
    for row in rows:
        subject_ids.append(row[subject_id_column])

    consent_dates = fetch_consent_dates(subject_ids)
    panels = fetch_panels('clinical-componenet-to-loinc.xml',
                          'translationTable.xml')
    # panels = {
    #     'rna': [1230],
    #     'cbc': [600, 712, 372]
    # }
    grouped_by_panel = group_rows_by_panel(panels, rows)
    # grouped_by_panel = {
    #     'rna': [<csv_row>, <csv_row>, <csv_row>],
    #     'cbc': [],
    #     'NONE': [<csv_row>, <csv_row>]
    # }
    filtered = filter_old_labs(grouped_by_panel, consent_dates)
    save(filtered)


def backup(filepath):
    # shutil.copy2(filepath, filepath + '.bak')
    raise NotImplementedError()


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


def save(rows):
    raise NotImplementedError()


if __name__ == "__main__":
    main()
