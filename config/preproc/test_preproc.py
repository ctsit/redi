import unittest

import preproc

STUDY_ID = 'STUDY_ID'
COMPONENT_ID = 'COMPONENT_ID'


class PreprocessingTests(unittest.TestCase):
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
            'cbc': [rows[2], rows[3]]
        }

        grouped = preproc.group_rows_by_panel(panels, rows)

        self.assertDictEqual(expected, grouped)


def do_nothing(*args, **kwargs):
    pass

if __name__ == '__main__':
    unittest.main()
