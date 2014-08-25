from lxml import etree
from redcap import Project, RedcapError
from requests import RequestException
import pprint
import redi_email
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class redcapClient:
    # Helper class for getting data from redcap instace

    project = None
    """
    __init__:
    This constructor in redcapClient takes a SimpleConfigParser object and establishes connection with REDCap instance.
    Parameters:
        settings: an object of class SimpleConfigParser (in SimpleConfigParser module) that is used for parsing configuration details
    """

    def __init__(self, redcap_uri,token) :

        self.redcap_uri = redcap_uri
        msg = 'Initializing redcap interface for: ' + redcap_uri
        logger.info(msg)
        self.token = token

        try:
            self.project = Project(redcap_uri, token)
            logger.info("redcap interface initialzed")
        except (RequestException,RedcapError) as e:
            logger.exception(e.message)
            raise

    """
    get_data_from_redcap:
    This function is used to get data from the REDCap instance
    Parameters:
        records_to_fetch    : a list object containing records
        events_to_fetch     : a list object containing events
        fields_to_fetch     : a list object containing fields
        forms_to_fetch      : a list object containing forms
        return_format       : specifies the format of the REDCap response. Default value is xml
    """

    def get_data_from_redcap(
            self,
            records_to_fetch=None,
            events_to_fetch=None,
            fields_to_fetch=None,
            forms_to_fetch=None,
            return_format='xml'):
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

    """
    send_data:
    This function is used to send data to the REDCap instance
    Parameters:
        data: This parameter contains the data that should be sent to the REDCap instance.
    """

    def send_data_to_redcap(self, data, overwrite = False) :
        #logger.info('Sending data for subject id: ' + data[0]['dm_subjid'])
        #logger.info(data)
        overwrite_value = 'normal'

        if overwrite:
            overwrite_value = 'overwrite'

        try:
            response = self.project.import_records(data, overwrite = overwrite_value)
            return response
        except RedcapError as e:
            logger.debug(e.message)
            raise
