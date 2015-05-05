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
import os
import tempfile
from redi import redi
import shutil


class TestGetDBPath(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_db_path(self):
        db_path = tempfile.mkdtemp()
        batch_info_database = "database.db"
        redi.get_db_path(batch_info_database, db_path)
        full_db_path = os.path.join(batch_info_database, db_path)
        assert os.path.exists(full_db_path) == 1
        shutil.rmtree(full_db_path)

    def test_get_db_path_not_exists(self):
        # verify that db path is created if it doesn't exist
        db_path =  "nonExistentPath"
        batch_info_database = "database.db"
        created_db_path = redi.get_db_path(batch_info_database, db_path)
        assert created_db_path ==  os.path.join(db_path, batch_info_database)
        shutil.rmtree(db_path)

if __name__ == '__main__':
    unittest.main()
