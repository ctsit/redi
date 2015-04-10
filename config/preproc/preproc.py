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


def main():
    run_processing()


def run_processing():
    backup('raw.txt')
    rows = csv.DictReader('raw.txt')
    subject_ids = list()
    for row in rows:
        subject_ids.append(row['STUDY_ID'])

    consent_dates = fetch_consent_dates(mrns)
    panels = fetch_panels('clinical-componenet-to-loinc.xml', 'translationTable.xml')
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
    save(filter_old_labs(grouped_records, consent_dates))


if __name__ == "__main__":
    main()
