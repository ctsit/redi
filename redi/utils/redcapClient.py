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

import logging
import time
import sys

from redcap import Project, RedcapError
from requests import RequestException
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError

# Configure module's logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RedcapClient(object):
    """ Client for a REDCap server.

    :param redcap_uri: URI for to REDCap server's API
    :param token: API Token for a REDCap project.
    :param verify_ssl: verify the SSL certificate? (default: True)
    :raises RedcapError: if we failed to get the project's metadata
    :raises RequestException: if some other network-related failure occurs
    """
    def __init__(self, redcap_uri, token, verify_ssl=True):
        self.redcap_uri = redcap_uri
        msg = 'Initializing redcap interface for: ' + redcap_uri
        logger.info(msg)
        self.token = token
        self.verify_ssl = verify_ssl

        try:
            self.project = Project(redcap_uri, token, "", verify_ssl)
            logger.info("redcap interface initialzed")
        except (RequestException, RedcapError) as e:
            logger.exception(e.message)
            raise

    def get_data_from_redcap(
            self,
            records_to_fetch=None,
            events_to_fetch=None,
            fields_to_fetch=None,
            forms_to_fetch=None,
            return_format='xml'):
        """ Exports REDCap records.

        :param records_to_fetch: if specified, only includes records in this
            list. Otherwise, includes all records.
        :type records_to_fetch: list or None

        :param events_to_fetch: if specified, only includes events in this list.
            Otherwise, includes all events.
        :type events_to_fetch: list or None

        :param fields_to_fetch: if specified, only includes fields in this list.
            Otherwise, includes all fields
        :type fields_to_fetch: list or None

        :param forms_to_fetch: if specified, only includes forms in this list.
            Otherwise, includes all forms.
        :type forms_to_fetch: list or None

        :param return_format: specifies the format of the REDCap response
            (default: xml)

        :return: response
        """
        logger.info('getting data from redcap')
        try:
            response = self.project.export_records(
                records=records_to_fetch,
                events=events_to_fetch,
                fields=fields_to_fetch,
                forms=forms_to_fetch,
                format=return_format)
        except RedcapError as e:
            logger.debug(e.message)
        return response

    def send_data_to_redcap(self, data, max_retry_count, overwrite=False,
        retry_count=0):
        """ Sends records to REDCap.

        :param list of dict objects data: records to send.
        :param bool overwrite: treat blank values as intentional?
            (default: False) When sending a record, if a field is blank, by
            default REDCap will not overwrite any existing value with a blank.
        :return: response
        :raises RedcapError: if failed to send records for any reason.
        :If MaxRetryError is caught, the function will try resending the same
         data for a maximum of max_retry_count times before exitting. For each
         attempt the wait time before sending is (the_attempt_no * 6)
        """
        overwrite_value = 'overwrite' if overwrite else 'normal'

        try:
            # The following line simulates github issue #108:
            # raise MaxRetryError('', 'localhost:8998', None)
            # The following line simulates 
            #raise NewConnectionError('localhost:8998', 443)
            response = self.project.import_records(data,
                overwrite=overwrite_value)
            return response
        except (MaxRetryError, NewConnectionError, ConnectionError) as e:
            logger.error("Exception encountered: ", exc_info = True)
            logger.debug(str(e.message) + ", Attempt no.: " + str(retry_count))
            if (retry_count == max_retry_count):
                message = "Exiting since network connection timed out after"\
                " reaching the maximum retry limit for resending data."
                logger.debug(message)
                sys.exit(message)
            # wait for some time before resending data
            time.sleep(retry_count*6)
            self.send_data_to_redcap(data, max_retry_count, 'overwrite',
                retry_count+1)
        except RedcapError as e:
            logger.debug(e.message)
            raise
