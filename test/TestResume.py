import unittest
# DO NOT IMPORT redi here!
# Each test needs it's own redi module so we can manipulate the
# module-scoped variables and functions


class TestResume(unittest.TestCase):

    def test_resume_switch(self):
        import bin.redi
        redi = reload(bin.redi)

        args = redi.parse_args('--verbose --dryrun'.split())
        self.assertFalse(args['resume'])

        args = redi.parse_args('--resume --verbose --dryrun'.split())
        self.assertTrue(args['resume'])

    def test_no_resume_deletes_old_run_data(self):
        class MockPersonFormEvents(object):
            def delete(self):
                raise FileDeleted()

        class FileDeleted():
            pass

        import bin.redi
        redi = reload(bin.redi)

        redi._person_form_events_service = MockPersonFormEvents()
        redi._check_input_file = lambda *args: None

        with self.assertRaises(FileDeleted):
            redi._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(), data_folder=None, database_path=None)

    def test_no_resume_stores(self):
        class MockPersonFormEvents(object):
            def delete(self):
                pass

            def store(self, ignored):
                raise FileStored()

        class FileStored():
            pass

        import bin.redi
        redi = reload(bin.redi)

        redi._person_form_events_service = MockPersonFormEvents()
        redi._check_input_file = lambda *args: None
        redi._create_person_form_event_tree_with_data = lambda *args: (None, None, None, None)
        redi._delete_last_runs_data = lambda *args: None
        redi._removedirs = lambda *args: None
        redi._mkdir = lambda *args: None

        with self.assertRaises(FileStored):
            redi._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(), data_folder=None, database_path=None)

    def test_resume_fetches_data_from_last_run(self):
        class MockPersonFormEvents(object):
            def fetch(self):
                raise DataFetched()

        class DataFetched():
            pass

        import bin.redi
        redi = reload(bin.redi)

        redi._person_form_events_service = MockPersonFormEvents()
        redi._check_input_file = lambda *args: None

        with self.assertRaises(DataFetched):
            redi._run(config_file=None, configuration_directory='',
                      do_keep_gen_files=None, dry_run=True, get_emr_data=False,
                      settings=MockSettings(), data_folder=None, database_path=None, resume=True)


class MockSettings(object):
    def __getattr__(self, item):
        return '' if ('file' in item) else None
