#!/usr/bin/env python

# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

import unittest
# DO NOT IMPORT redi here!
# Each test needs it's own redi module so we can manipulate the
# module-scoped variables and functions


class TestResume(unittest.TestCase):

    def test_no_resume_deletes_old_run_data(self):
        class MockPersonFormEvents(object):
            def delete(self):
                raise FileDeleted()

        class FileDeleted():
            pass

        import redi.redi
        redi_ref = reload(redi.redi)
        redi_ref._person_form_events_service = MockPersonFormEvents()

        import redi.batch
        batch = reload(redi.batch)
        batch.check_input_file = lambda *args: None

        with self.assertRaises(FileDeleted):
            redi_ref._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(),  data_folder=None,
                      database_path=None, raw_txt_file = None, redcap_client=None,
                      report_courier=None, report_creator=None)

    def test_no_resume_stores(self):
        class MockPersonFormEvents(object):
            def delete(self):
                pass

            def store(self, ignored):
                raise FileStored()

        class FileStored():
            pass

        import redi.redi
        redi_ref = reload(redi.redi)

        redi_ref._person_form_events_service = MockPersonFormEvents()
        redi_ref._create_person_form_event_tree_with_data = lambda *args: (
            None, None, None, None, None)
        redi_ref._delete_last_runs_data = lambda *args: None
        redi_ref._removedirs = lambda *args: None
        redi_ref._mkdir = lambda *args: None
        redi_ref.connect_to_redcap = lambda *args: None

        import redi.batch
        batch = reload(redi.batch)
        batch.check_input_file = lambda *args: None

        with self.assertRaises(FileStored):
            redi_ref._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(), data_folder=None, raw_txt_file = None,
                      database_path=None, redcap_client=None,
                      report_courier=None, report_creator=None)

    def test_resume_fetches_data_from_last_run(self):
        class MockPersonFormEvents(object):
            def fetch(self):
                raise DataFetched()

        class DataFetched():
            pass

        import redi.redi
        redi_ref = reload(redi.redi)
        redi_ref._person_form_events_service = MockPersonFormEvents()

        import redi.batch
        batch = reload(redi.batch)
        batch.check_input_file = lambda *args: None

        with self.assertRaises(DataFetched):
            redi_ref._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(), data_folder=None, raw_txt_file = None,
                      database_path=None, resume=True, redcap_client=None,
                      report_courier=None, report_creator=None)


class MockSettings(object):
    def __getattr__(self, item):
        return '' if ('file' in item) else None

if __name__ == '__main__':
    unittest.main()
