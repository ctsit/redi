import contextlib
import csv
import StringIO
import os
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
"PanelA_Test1","11","7.2","4.0","10.0","thou/cu mm","2012-06-21 13:30:00","2012-06-23 00:00:00","302"
"PanelB_Test1","21","123.1","4.0","10.0","IU/mL","2012-06-20 13:30:00","2012-06-22 00:00:00","303"
"""

STUDY_ID = 'STUDY_ID'
COMPONENT_ID = 'COMPONENT_ID'


class PreprocessingTests(unittest.TestCase):
    def test_fetch_panels(self):
        loinc_map_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '../clinical-component-to-loinc-code-example.xml'))
        translation_table_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../translationTable.xml'))

        panels = preproc.fetch_panels(loinc_map_file, translation_table_file)

        self.assertDictEqual({
            'cbc': ['26515-7', '718-7', '26474-7', '26499-4', '26464-8'],
            'chemistry': ['1975-2', '2160-0', '2339-0', '1920-8', '1968-7',
                          '1751-7', '1742-6', '2947-0', '6298-4']},
            panels)

    def test_group_rows_by_panel(self):
        panels = {
            'rna': [1230],
            'cbc': [600, 712, 372]
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

        grouped = preproc.group_rows_by_panel(panels, rows)

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


if __name__ == '__main__':
    unittest.main()
