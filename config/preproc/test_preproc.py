import contextlib
import csv
import datetime
import os
import StringIO
import unittest

import preproc

results_input = """
"NAME","COMPONENT_ID","ORD_VALUE","REFERENCE_LOW","REFERENCE_HIGH","REFERENCE_UNIT","SPECIMN_TAKEN_TIME","RESULT_DATE","STUDY_ID"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","301"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","302"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","303"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-21 13:30:00","2012-06-23 00:00:00","303"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-21 13:30:00","2012-06-23 00:00:00","302"
"PanelB_Test1","21","123.1","4.0","10.0","IU/mL","2012-06-20 13:30:00","2012-06-22 00:00:00","303"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-20 13:30:00","2012-06-22 00:00:00","303"
"""

expected = """
"NAME","COMPONENT_ID","ORD_VALUE","REFERENCE_LOW","REFERENCE_HIGH","REFERENCE_UNIT","SPECIMN_TAKEN_TIME","RESULT_DATE","STUDY_ID"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","301"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","302"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-22 13:30:00","2012-06-24 00:00:00","303"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-21 13:30:00","2012-06-23 00:00:00","303"
"PanelB_Test1","21","123.1","4.0","10.0","IU/mL","2012-06-20 13:30:00","2012-06-22 00:00:00","303"
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-21 13:30:00","2012-06-23 00:00:00","302"
"""

STUDY_ID = 'STUDY_ID'
COMPONENT_ID = 'COMPONENT_ID'
TAKEN_TIME = 'TAKEN_TIME'


class PreprocessingTests(unittest.TestCase):
    def test_fetch_panels(self):
        loinc_map_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../clinical-component-to-loinc-code-example.xml'))
        translation_table_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../translationTable.xml'))

        panels = preproc.fetch_panels(loinc_map_file, translation_table_file)

        self.assertDictEqual({
            'cbc': ['26515-7', '26464-8', '26474-7', '718-7', '26499-4'],
            'chemistry': ['1975-2', '2160-0', '2339-0', '1920-8', '6298-4',
                          '1968-7', '1751-7', '1742-6', '2947-0']},
            panels)

    def test_filter_old_labs(self):
        panel = [
            {STUDY_ID: '304', COMPONENT_ID: '1230', TAKEN_TIME: '2012-06-23',
             'data': '123'},
            {STUDY_ID: '304', COMPONENT_ID: '1230', TAKEN_TIME: '2012-06-20',
             'data': 'Yes?'},
            {STUDY_ID: '304', COMPONENT_ID: '1230', TAKEN_TIME: '2012-06-22',
             'data': '456'},
            {STUDY_ID: '304', COMPONENT_ID: '1230', TAKEN_TIME: '2012-06-21',
             'data': '789'},
            {STUDY_ID: '304', COMPONENT_ID: '630', TAKEN_TIME: '2012-06-21',
             'data': 'yes'},
        ]

        rows_grouped_by_panel = {'PanelA': panel}
        consent_dates = {'304': '2012-06-23'}
        previous = preproc.TAKEN_TIME_COLUMN, preproc.SUBJECT_ID_COLUMN
        preproc.TAKEN_TIME_COLUMN = TAKEN_TIME
        preproc.SUBJECT_ID_COLUMN = STUDY_ID

        filtered = preproc.filter_old_labs(rows_grouped_by_panel, consent_dates)

        preproc.TAKEN_TIME_COLUMN, preproc.SUBJECT_ID_COLUMN = previous

        self.assertListEqual([panel[0], panel[2], panel[3], panel[4]], filtered)

    def test_group_rows_by_panel(self):
        panels = {
            'rna': ['1230'],
            'cbc': ['600', '712', '372']
        }

        rows = [
            {STUDY_ID: '300', COMPONENT_ID: '1230', 'data': '123'},
            {STUDY_ID: '301', COMPONENT_ID: '1230', 'data': '456'},
            {STUDY_ID: '300', COMPONENT_ID: '600', 'data': '10'},
            {STUDY_ID: '301', COMPONENT_ID: '600', 'data': '11'},
            {STUDY_ID: '300', COMPONENT_ID: '000', 'data': 'Yes'}
        ]

        expected = {
            'rna': [rows[0], rows[1]],
            'cbc': [rows[2], rows[3]],
            'NONE': [rows[4]]
        }
        previous = preproc.COMPONENT_ID_COLUMN
        preproc.COMPONENT_ID_COLUMN = COMPONENT_ID

        grouped = preproc.group_rows_by_panel(panels, rows)

        preproc.COMPONENT_ID_COLUMN = previous

        self.assertDictEqual(expected, grouped)

    def test_save(self):
        output = StringIO.StringIO()

        @contextlib.contextmanager
        def open_memory(*args, **kwargs):
            yield output

        data = StringIO.StringIO(results_input.strip())
        reader = csv.DictReader(data)

        preproc.save(reader.fieldnames, reader, 'UNUSED', backup=None,
                     open_file=open_memory)

        self.assertTrue(results_input.strip(), str(output))

    def test_0_tests_before_baseline(self):
        preproc.run_processing()


if __name__ == '__main__':
    unittest.main()
