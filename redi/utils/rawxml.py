# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

import os.path
import time
import datetime

class RawXml(object):
    """
    This class is used to store details about the input file
    @see redi.batch.check_input_file()
    """

    def __init__(self, project, path):
        """
        Parameters
        ----------
        project : string
            The project name - the owner of the xml file
        path : string
            The xml file path
        """
        self._project = project
        self._path = path


    def get_project(self):
        return self._project

    def get_creation_time(self):
        """ Get the OS creation time """
        #tst = time.ctime(os.path.getctime(self._path))
        tst = os.path.getctime(self._path)
        return datetime.datetime.fromtimestamp(tst)


    def get_last_modified_time(self):
        """ Get the OS modification time """
        tst = os.path.getmtime(self._path)
        return datetime.datetime.fromtimestamp(tst)


    def get_info(self):
        """
        Return a string containing all details available about the xml file
        """
        info = """
Project name: {0}
File path: {1}
File created: {2}
File last modified: {3} """.format(self._project, \
            self._path, \
            self.get_creation_time(), \
            self.get_last_modified_time())
        return info
