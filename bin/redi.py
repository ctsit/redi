#/usr/bin/env python
"""

redi.py - Converter from raw clinical data in XML format to REDCap API data

"""
# Version 0.1 2013-11-18
__author__ = "Nicholas Rejack"
__copyright__ = "Copyright 2013, University of Florida"
__license__ = "BSD 2-Clause"
__version__ = "0.1"
__email__ = "nrejack@ufl.edu"
__status__ = "Development"


#import csv, sys
from lxml import etree
import logging
from collections import defaultdict
from collections import Counter
import string
import httplib
from urllib import urlencode
import os
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

# INTERMEDIATE STEPS: XML!
# step 1: parse raw XML to ElementTree: "data"
    # step 1b: call read-in function to load xml into ElementTree
# step 2: parse formEvents.xml to ElementTree
        # step 2b: call read-in function to load xml into ElementTree
# step 3: parse translationTable.xml to ElementTree
        # step 3b: call read-in function to load xml into ElementTree
# step 4: add element to data ElementTree for timestamp, redcap form name,
#    eventName,    formDateField, and formCompletedFieldName
    # step 4a: write out ElementTree as an XML file
    # step 4b: call read-in function to load xml into ElementTree
# step 5: update timestamp using collection_date and collection_time
# step 7: write redcapForm name to data ElementTree by a lookup of component ID
#            in translationTable.xml
# step 8: sort data by: study_id, form name, then timestamp, ascending order
# step 10: write formDateField to data ElementTree via lookup of formName
#                in formEvents.xml
# step 11: write formCompletedFieldName to data ElementTree via lookup of
#        formName in formEvents.xml
# step 12: write eventName to data ElementTree via lookup of formName in
#                    formEvents.xml
#    ex: <formName value="chemistry">
#            <event name="1_arm_1" />
#        </formName>
# step 13: write the Final ElementTree to EAV



def main():
    """main function. flow starts here
        Radha
    """
    # Configure logging
    configure_logging()
    logger.info('Logger configured')

    # read config
    setup_json = proj_root+'config/setup.json'
    setup = read_config(setup_json)
    
    # read in 3 main data files / translation tables
    raw_xml_file = proj_root+ setup['raw_xml_file']
    form_events_file = proj_root+ setup['form_events_file']
    translation_table_file = proj_root+ setup['translation_table_file']
    data_file_path = proj_root+ setup['data_file_path']
    report_parameters = {'report_file_path':proj_root+setup['report_file_path'],'project':setup['project'],'redcap_server':setup['redcap_server']}
    report_xsl = proj_root+ setup['report_xsl_path']
    send_email = setup['send_email']
    input_date_format = setup['input_date_format']
    output_date_format = setup['output_date_format']

    
    # Set path to log file
    # system_log_file = setup['system_log_file']

    # parse the raw.xml file and fill the etree rawElementTree
    data = parse_raw_xml(raw_xml_file)

    # check if raw element tree is empty
    if not data:
        # raise an exception if empty
        raise LogException('data is empty')

    # add blank elements to each subject in data tree
    add_elements_to_tree(data)

    # parse the formEvents.xml file and fill the etree 'form_events_file'
    form_events_tree = parse_form_events(form_events_file)
    forms = form_events_tree.findall("form/name")
    form_Completed_Field_Names = form_events_tree.findall("form/formCompletedFieldName")
    form_data = {}
    for i in range(len(forms)):
        form_data[forms[i].text] = form_Completed_Field_Names[i].text
    
    # check if form element tree is empty
    if not form_events_tree:
        # raise an exception if empty
        raise LogException('form_events_tree is empty')
    write_element_tree_to_file(form_events_tree, proj_root+'formData.xml')

    # parse the translationTable.xml file and fill the
    #    etree 'translation_table_file'
    global translational_table_tree
    translational_table_tree = parse_translation_table(translation_table_file)

    # check if translational table element tree is empty
    if not translational_table_tree:
        # raise an exception if empty
        raise LogException('translational_table_tree is empty')
    write_element_tree_to_file(translational_table_tree,
                              proj_root+'translationalData.xml')

    # update the timestamp for the global element tree
    update_time_stamp(data, input_date_format, output_date_format)
    # write back the changed global Element Tree
    write_element_tree_to_file(data, proj_root+'rawData.xml')

    # update the redcap form name
    update_redcap_form(data, translational_table_tree, 'undefined')
    # write the element tree
    write_element_tree_to_file(data, proj_root+'rawDataWithFormName.xml')

    # set all formImportedFieldName value to the value mapped from
    # formEvents.xml
    update_form_imported_field(data, form_events_tree, proj_root+'undefined')
    # output raw file to check it
    write_element_tree_to_file(data, proj_root+'rawDataWithFormImported.xml')

    # update the redcapFieldNameStatus
    update_recap_form_status(data, translational_table_tree, 'undefined')
    # output raw file to check it
    write_element_tree_to_file(data, proj_root+'rawDataWithFormStatus.xml')

    # update formDateField
    update_formdatefield(data, form_events_tree)
    # write back the changed global Element Tree
    write_element_tree_to_file(data, proj_root+'rawData.xml')

    ## update formCompletedFieldName
    update_formcompletedfieldname(data, form_events_tree, 'undefined')
    ## write back the changed global Element Tree
    write_element_tree_to_file(data, proj_root+'rawDataWithFormCompletedField.xml')

    # update element that holds the name of the redcap field that will hold
    # the datum or value.
    # Also update the name of the redcap field that will hold the units
    update_redcap_field_name_value_and_units(data, translational_table_tree,
                                                 'undefined')
    ## write back the changed global Element Tree
    write_element_tree_to_file(data, proj_root+'rawDataWithDatumAndUnitsFieldNames.xml')

    # sort the data tree
    sort_element_tree(data)
    write_element_tree_to_file(data, proj_root+'rawDataSorted.xml')


    # update eventName element
    alert_summary = update_event_name(data, form_events_tree, 'undefined')
    ## write back the changed global Element Tree
    write_element_tree_to_file(data, proj_root+'rawDataWithAllUpdates.xml')

    # generate redcap eav
    report_data = generate_redcap_eav(data,form_data,output_date_format)
    
    # pull the data from the generated eav and push it to redi
    try:
        data_file = open(data_file_path, 'r')
        data_to_post = data_file.read()
    except IOError:
        raise LogException('EAV '+data_file_path +' file not found')

    # Initialize RedI
    properties = init_redcap_interface(setup)

    # send data to redcap intereface
    send_data_to_redcap(properties, data=data_to_post, token=setup['token'])

    #create summary report
    xml_report_tree = create_summary_report(report_parameters, report_data, form_data, alert_summary)
    xslt = etree.parse(report_xsl)
    transform = etree.XSLT(xslt)
    html_report = transform(xml_report_tree)
    html_str = etree.tostring(html_report, method='html', pretty_print=True)
    
    # send report via email
    if send_email == 'Y':
        sender = setup["sender_email"]
        receiver = setup["receiver_email"]
        send_report(sender,receiver,html_str)
    

def get_emr_data():
    '''This function gets the EMR data from the sftp server and
        writes to a text file

    '''
    #from ftplib import FTP
    #ftp = FTP('')
    pass

def read_config(setup_json):
    """function to read the config data from setup.json
        Philip

    """
    import json

    try:
        json_data = open(setup_json)
    except IOError:
        #raise logger.error
        print "file " + setup_json + " could not be opened"
        raise

    setup = json.load(json_data)
    json_data.close()

    # test for required parameters
    required_parameters = ['translation_table_file', 'form_events_file',
                    'raw_xml_file', 'system_log_file', 'redcap_uri', 'token']
    for parameter in required_parameters:
        if not parameter in setup:
            raise LogException("read_config: required parameter, '"
            + parameter  + "', is not set in " + setup_json)

    # test for required files but only for the parameters that are set
    files = ['translation_table_file', 'form_events_file', 'raw_xml_file']
    for item in files:
        if item in setup:
            if not os.path.exists(proj_root + setup[item]):
                raise LogException("read_config: " + item + " file, '"
                        + setup[item] + "', specified in "
                        + setup_json + " does not exist")
    return setup

def parse_raw_xml(raw_xml_file):
    """Generate an ElementTree from a raw XML file.

    Keyword argument:
    raw_xml_file: the input file.

    written by: Nicholas

    """
    if not os.path.exists(raw_xml_file):
        raise LogException("Error: raw xml file not found at file not found at "
            + raw_xml_file)
    else:
        raw = open(raw_xml_file, 'r')
        logger.info("Raw XML file read in. " +  str(sum(1 for line in raw))
            + " total lines in file.")
    data = etree.parse(raw_xml_file)
    event_sum = len(data.findall(".//subject"))
    logger.info(str(event_sum) + " total subject entries read into tree.")
    raw.close()
    logger.info("Raw XML file closed.")
    return data

def parse_form_events(form_events_file):
    """Parse the form_events file into an ElementTree.

    Keyword argument:
    form_events_file: the form_events XML file.
    Read from the JSON configuration.

    written by Nicholas
    """
    if not os.path.exists(form_events_file):
        raise LogException("Error: form events file not found at "
            + form_events_file)
    else:
        raw = open(form_events_file, 'r')
        logger.info("Form events file read in. " +  str(sum(1 for line in raw))
            + " total lines in file.")
    data = etree.parse(form_events_file)
    event_sum = len(data.findall(".//event"))
    logger.info(str(event_sum) + " total events read into tree.")
    raw.close()
    logger.info("Form events file closed.")
    return data


def parse_translation_table(translation_table_file):
    '''function to parse translationTable.xml to ElementTree
        returns an ElementTree
        Nicholas

    '''
    if not os.path.exists(translation_table_file):
        raise LogException("Error: translation table file not found at "
            + translation_table_file)
    else:
        raw = open(translation_table_file, 'r')
        logger.info("Translation table file read in. "
            +  str(sum(1 for line in raw)) + " total lines in file.")
    data = etree.parse(translation_table_file)
    event_sum = len(data.findall(".//clinicalComponent"))
    logger.info(str(event_sum) + " total clinicalComponents read into tree.")
    raw.close()
    logger.info("Translation table file closed")
    return data

def add_elements_to_tree(data):
    """Add blank elements to fill out in ElementTree.

    Keyword argument:
    data: the input ElementTree from the parsed raw XML file.

    add element to data ElementTree for timestamp, redcap form name, eventName,
    formDateField, and formCompletedFieldName.

    Written by Nicholas.
    """
    for element in data.iter('subject'):
        element.append(etree.Element("timestamp"))
        element.append(etree.Element("redcapFormName"))
        element.append(etree.Element("eventName"))
        element.append(etree.Element("formDateField"))
        element.append(etree.Element("formCompletedFieldName"))
        element.append(etree.Element("formImportedFieldName"))
        element.append(etree.Element("redcapFieldNameValue"))
        element.append(etree.Element("redcapFieldNameUnits"))
        element.append(etree.Element("redcapFieldNameStatus"))

def update_recap_form_status(data, lookup_data, undefined):
    '''This function updates the redcapFieldNameStatus value
        to all the subjects
        Radha

    '''
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapFieldNameStatus'
    index_element_in_data = 'COMPONENT_ID'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'clinicalComponentId'
    value_in_lookup_data = 'redcapFieldNameStatus'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

def update_form_imported_field(data, lookup_data, undefined):
    '''This function updates the formImportedFieldName value
        to all the subjects
        Radha

    '''
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'formImportedFieldName'
    index_element_in_data = 'redcapFormName'
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    value_in_lookup_data = 'formImportedFieldName'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

def write_element_tree_to_file(element_tree, file_name):
    '''function to write ElementTree to a file
        takes file_name as input
        Radha

    '''
    logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(file_name, encoding="us-ascii", xml_declaration=True,
            method="xml")


def update_time_stamp(data, input_date_format, output_date_format):
    '''function to update timestamp using input and output data formats
        reads from raw ElementTree and writes to it
        Radha

    '''
    import time
    logger.info('Updating timestamp to ElementTree')
    for subject in data.iter('subject'):
        # New EMR field SPECIMN_TAKEN_TIME is used in place of Collection Date and Collection Time
        specimn_taken_time = subject.find('SPECIMN_TAKEN_TIME').text
        
        if specimn_taken_time is not None:
            #Converting specimen taken time to redcap accepted time format YYYY-MM-DD
            
            # construct struct_time structure from String
            # this will accurately pad each part of the time
            # Rule : generic input/output of date format
            temptime = time.strptime(specimn_taken_time, input_date_format)
            # convert struct into a string representation
            date_time = time.strftime(output_date_format, temptime)
            
            # write the dateTime to ElementTree
            subject.find('timestamp').text = format(date_time)


def update_redcap_form(data, lookup_data, undefined):
    '''function to lookup component ID in translationTable to get
        redcapFormName.
        writes the redcapForm name to data
        If component lookup fails, sets formName to undefinedForm
        Philip

    '''
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapFormName'
    index_element_in_data = 'COMPONENT_ID'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'clinicalComponentId'
    value_in_lookup_data = 'redcapFormName'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

def sort_element_tree(data):
    """Sort element tree based on three given indices.

    Keyword argument: data
    sorting is based on study_id, form name, then timestamp, ascending order

    """

    # this element holds the subjects that are being sorted
    container = data.getroot()
    container[:] = sorted(container, key=getkey)

def getkey(elem):
    """Helper function for sorting. Returns keys to sort on.

    Keyword argument: elem
    returns the corresponding tuple study_id, form_name, timestamp

    Nicholas

    """
    study_id = elem.findtext("STUDY_ID")
    form_name = elem.findtext("redcapFormName")
    timestamp = elem.findtext("timestamp")
    return (study_id, form_name, timestamp)


def update_formdatefield(data, form_events_tree):
    '''function to write formDateField to data ElementTree via lookup of
        formName in formEvents ElementTree
        Radha

    '''
    logger.info('updating the formDateField')
    # make a dictionary of the relevant elements from the translationTable
    form_event_root = form_events_tree.getroot()
    if form_event_root is None:
        raise LogException('Form Events tree is empty')
    form_events_dict = dict()
    for child in form_event_root.iter('form'):
        form_events_dict[child.find('name').text] = \
                        child.find('formDateField').text
    # final element tree's root
    data_root = data.getroot()

    # iterate thru each subject
    for subject in data_root.iter('subject'):
        # get the value of formDateField for a given formName from
        # [redcapFormName, formDateField] dictionary
        form_name = subject.find('redcapFormName').text
        default_value = 'undefined'
        if form_name == default_value:
            subject.find('formDateField').text = default_value
            continue
        try:
            # fill the 'undefined' value if the formname is not found
            subject.find('formDateField').text = form_events_dict.get\
            (form_name, default_value)
        except KeyError:
            #print form_name
            #print('key not found')
            logger.error('formName is empty. so not updating formDateField')
            continue


def update_formcompletedfieldname(data, lookup_data, undefined):
    '''function to update formCompletedFieldName in data ElementTree via
        lookup of formName in formEvents ElementTree

    '''
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'formCompletedFieldName'
    index_element_in_data = 'redcapFormName'
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    value_in_lookup_data = 'formCompletedFieldName'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)


def update_redcap_field_name_value_and_units(data, lookup_data, undefined):
    '''function to update redcapFieldNameValue and
        redcapFieldNameUnits in data
        ElementTree via lookup of redcapFieldNameValue and
        redcapFieldNameUnits in
        translation table tree

    '''
    # set redcapFieldNameValue
    element_to_set_in_data = 'redcapFieldNameValue'
    index_element_in_data = 'COMPONENT_ID'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'clinicalComponentId'
    value_in_lookup_data = 'redcapFieldNameValue'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

    # set redcapFieldNameUnits
    element_to_set_in_data = 'redcapFieldNameUnits'
    index_element_in_data = 'COMPONENT_ID'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'clinicalComponentId'
    value_in_lookup_data = 'redcapFieldNameUnits'
    undefined = "redcapFieldNameUnitsUndefined"

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)



def update_data_from_lookup(data, element_to_set_in_data,
    index_element_in_data, lookup_data, element_to_find_in_lookup_data,
    index_element_in_lookup_data, value_in_lookup_data, undefined):
    '''Update a single field in an element tree based on a lookup in another
        element tree
        Parameters:
        data - an element tree with a field that needs to be set
        element_to_set_in_data - element that will be set
        index_element_in_data - element in data that wil be looked up
                in lookup table where value of element to be set wil be found
        lookup_data - an element tree that contains, the lookup data
        element_to_find_in_lookup_data - parameter for the initial
                findall in the lookup data
        index_element_in_lookup_data - the element in the lookup data
                that will be the key in the lookup table
        value_in_lookup_data - element in the lookup data that provides
                the value in the lookup table
        undefined - a string to be returned for all failed lookups in
                the lookup table

    '''

    # make a dictionary of the relevant elements from the lookup table
    root_of_lookup_data = lookup_data.getroot()
    lookup_table = dict()
    for child in root_of_lookup_data.findall(element_to_find_in_lookup_data):
        child_lookup_data = child.find(value_in_lookup_data)
        if child_lookup_data is not None:
            lookup_table[child.find(index_element_in_lookup_data).text] = \
                        child_lookup_data.text
    # Update the field value using the lookup_table we just created
    data_root = data.getroot()
    for child in data_root:
        # get the element text, but set a default value of undefined for
        # each look up failure
        new_element_text = \
            lookup_table.get(child.find(index_element_in_data).text, undefined)
        element_to_set = child.find(element_to_set_in_data)
        element_to_set.text = new_element_text



def update_event_name(data, lookup_data, undefined):
    '''function to update eventName to data ElementTree via lookup of formName
        in formEvents ElementTree

    '''
    # make a dictionary of form_events
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    list_element_in_lookup_data = 'event'
    root_of_lookup_data = lookup_data.getroot()
    lookup_table = defaultdict(list)

    for child in root_of_lookup_data.findall(element_to_find_in_lookup_data):
        key = child.find(index_element_in_lookup_data).text
        for grandchild in child.findall(list_element_in_lookup_data):
            lookup_table[key].append(grandchild.find('name').text)

    # Recurse over study records setting eventName on each record with
    # a defined form
    element_to_set_in_data = 'eventName'
    last_record_group = 'dummy'
    last_timestamp_group = 'dummy'
    event_index = 0
    lookup_table_length = 1
    old_form_name = 'dummy'
    distinct_value = Counter()

    # initialize the Maximum events alert
    max_event_alert = []
    # initialize the Multiple values for same key alert
    multiple_values_alert = []
    # sample alerts
    #max_event_alert.append('this is sample max event alert')
    #multiple_values_alert.append('this is sample multiple values alert')

    for subject in data.getroot():
        study_id = subject.findtext("STUDY_ID")
        form_name = subject.findtext("redcapFormName")
        timestamp = subject.findtext("timestamp")
        redcap_field_name_value = subject.findtext("redcapFieldNameValue")
        collection_time = subject.findtext("Collection_Time")

        element_to_set = subject.find(element_to_set_in_data)
        # if the form_name 'undefined, go to the next record!
        if form_name == 'undefined':
            # log something as info
            element_to_set.text = undefined
        elif timestamp == '':
            # Log this as bad data we are skipping
            logger.warn("update_event_name: timestamp is missing.  Skipping form %s for subject %s", \
                form_name, study_id)
        else:
            lookup_table_length = len(lookup_table[form_name])
            current_record_group = string.join([study_id, form_name], "_")
            current_timestamp_group = \
                    string.join([study_id, form_name, timestamp], "_")
            if last_record_group != current_record_group:
                #Check that the event counter form the previous loop did not
                # exceed the size of the event list.  If it did we should
                # issue a warning
                
                if event_index >= lookup_table_length:
                    max_event_alert.append("Exceeded event list for record group "+\
                                        last_record_group+ ". Event count of "+str(event_index)+\
                                " exceeds maximum of "+str(len(lookup_table[old_form_name])))
                    logger.warn('update_event_name: %s', max_event_alert)
                
                # reset the event counter so we can restart from the top
                # of the list. We have moved to a new group
                logger.debug("update_event_name: Move to new record group: %s",
                    current_record_group)
                logger.debug("update_event_name: Move to new record group: \
                        changing last_timestamp_group %s",
                            current_timestamp_group)

                last_record_group = current_record_group
                last_timestamp_group = current_timestamp_group
                event_index = 0
            if last_timestamp_group != current_timestamp_group:
                # move to the next event
                logger.debug("update_event_name: Move to next event: " +
                    current_timestamp_group)
                event_index += 1
                last_timestamp_group = current_timestamp_group
            else:
                pass
            # note which form we were on
            old_form_name = form_name
            # check that we have not exceeded the event count for this form.
            # If we have we must issue a warning
            if event_index < lookup_table_length:
                logger.debug("update_event_name: eventName: %s event_index: %s\
                redcapFieldName: %s current_timestamp_group: %s",
                str(lookup_table[form_name][event_index]), str(event_index),
                    redcap_field_name_value, str(current_timestamp_group))
                element_to_set.text = lookup_table[form_name][event_index]

                # Increment a counter for each distinct value and test if
                # it is still distinct
                connector_string = "_"
                if study_id is None:
                    study_id = 'none'
                if form_name is None:
                    form_name = 'none'
                if redcap_field_name_value is None:
                    redcap_field_name_value = 'none'
                if timestamp is None:
                    timestamp = 'none'
                if collection_time is None:
                    collection_time = 'none'
                field_key = connector_string.join([study_id, form_name, \
                        redcap_field_name_value, timestamp, collection_time])
                #print field_key
                distinct_value[field_key] += 1
                if distinct_value[field_key] > 1:
                    multiple_values_alert.append('Multiple values found for field '+\
                                                            field_key)
                    logger.warn("update_event_name: multiple values \
                        found for field %s", field_key)
            else:
                element_to_set.text = undefined
                logger.debug("update_event_name: lookup_table_length exceeded.\
                  event_index: %s", str(event_index))
    return {'max_event_alert':max_event_alert, 'multiple_values_alert':multiple_values_alert}


def generate_redcap_eav(data,form_data,output_date_format):
    '''function to generate REDCap EAV from data ElementTree

    '''
    #import csv

    eav_file = open(proj_root+'config/redcap.eav', 'w')

    # prepare the header format of the EAV file to be generated
    header = "record,redcap_event_name,field_name,value\n"
    # write the field names the top of EAV file
    eav_file.write(header)
    report_data = {}
    consolidated_form_data = {}
    total_form_counts = {}
    for v in form_data.values():
        total_form_counts[v] = 0
        consolidated_form_data[v] = {}
    subject_dates = {}
    all_dates = set()
    total_cbc_count = 0
    total_chem_count = 0
    # write the rows of data
    last_record_group = 'dummy'
    component_list = []
    last_record_group_list = {'study_id':'',
                                'event_name':'',
                                'form_name':'',
                                'field_name':''}
    # initialize status dictionary from the translational table tree
    status_dict = init_statusdict()
    for subject in data.getroot():
        eav_str = ''
        study_id = subject.findtext("STUDY_ID")
        form_name = subject.findtext("redcapFormName")
        event_name = subject.findtext("eventName")
        timestamp = subject.findtext("timestamp")
        for k in consolidated_form_data.keys():
            if study_id not in consolidated_form_data[k]:
                consolidated_form_data[k][study_id] = 0
        if study_id not in subject_dates:
            subject_dates[study_id] = list()

        # if the form_name 'undefined, go to the next record!
        # TIMESTAMP check below is just a work-around for skipping the 
        # wrong input of empty timestamps
        if form_name == 'undefined' or event_name == 'undefined' or timestamp == '':
            pass
            # log something as info
        else:
            current_record_group = \
                string.join([study_id, form_name, event_name], "_")
            redcap_field_name_value = subject.findtext("redcapFieldNameValue")
            redcap_field_name_units = subject.findtext("redcapFieldNameUnits")
            reference_unit = subject.findtext("REFERENCE_UNIT")
            form_date_field = subject.findtext("formDateField")
            form_completed_field_name = \
                subject.findtext("formCompletedFieldName")
            form_imported_field_name = \
                subject.findtext("formImportedFieldName")
            redcap_form_status = \
                subject.findtext("redcapFieldNameStatus")
            result_value = subject.findtext("ORD_VALUE")
            
            
            #rule_engine(last_record_group)
            #print last_record_group+' '+current_record_group
            #print last_record_group_list
            #print last_record_group_list['form_name']
            if last_record_group != current_record_group:
                # send the component_list to rules engine
                #print component_list
                initialize_componentdict()
                #print component_list
                component_dict = rule_engine(component_list, last_record_group_list['form_name'])
                
                if component_dict is None:
                    logger.error('Returned null component dictionary')
                    last_record_group = current_record_group
                    continue
                # output the last records form statuses
                stat = 'YES'
                #print last_record_group_list['field_name']
                #print component_dict
                #print last_record_group_list['form_name']
                #if component_dict is not None:
                for myfield, myvalue in component_dict.iteritems():
                    #print str(myfield) + " " + str(myvalue)
                    if myvalue is False and status_dict[myfield] is not None:
                        stat = 'NOT_DONE'
                        eav_str = \
                        last_record_group_list['study_id'] + ',"' + \
                        last_record_group_list['event_name'] + '",' + \
                        str(status_dict[myfield]) +',"' +\
                        stat + '"\n'
                        eav_file.write(eav_str.encode('utf-8'))
                del component_list[:]
                

                # output event date and form completed records
                #print current_record_group+' '+redcap_field_name_value+' '+timestamp
                # For event date records, output the fields
                #   Study_Id,eventName,formDateField,timestamp
                all_dates.add(last_record_group_list['timestamp'])
                subject_dates[study_id].append(last_record_group_list['timestamp'])
                eav_str = \
                    last_record_group_list['study_id'] + ',"' + \
                    last_record_group_list['event_name'] + '",' + \
                    last_record_group_list['form_date_field'] + ',"' + \
                    last_record_group_list['timestamp'] + '"\n'
                eav_file.write(eav_str.encode('utf-8'))

                
                completed_field_name = last_record_group_list['form_completed_field_name']
                if completed_field_name in form_data.values():
                    total_form_counts[completed_field_name] = \
                    total_form_counts[completed_field_name] + 1
                    consolidated_form_data[completed_field_name][last_record_group_list['study_id']] = \
                    consolidated_form_data[completed_field_name][last_record_group_list['study_id']] +1

                # For form completed records, output the fields
                #   Study_Id,eventName,formCompletedFieldName, 2
                eav_str = last_record_group_list['study_id'] + ',"' + \
                    last_record_group_list['event_name'] + '",' + \
                    last_record_group_list['form_completed_field_name'] + ',2\n'
                eav_file.write(eav_str.encode('utf-8'))

                # For form imported records, output the fields
                #   Study_Id,eventName,formImportedFieldName, yes
                #  NOT_DONE -> NO | null -> YES
                if last_record_group_list['form_imported_field_name'] != 'undefined' :
                    eav_str = last_record_group_list['study_id'] + ',"' + \
                        last_record_group_list['event_name'] + '",' + \
                        last_record_group_list['form_imported_field_name'] + ',"Y"\n'
                    eav_file.write(eav_str.encode('utf-8'))

                # done with last record group and moving to new record
                # re-initialize last record in list
                #del last_record_group_list

            # note that we have moved to a new group
            last_record_group = current_record_group
            #if last_record_group == current_record_group:
            #print redcap_field_name_value
            last_record_group_list['study_id'] = study_id
            last_record_group_list['event_name'] = event_name
            last_record_group_list['form_name'] = form_name
            last_record_group_list['field_name'] = redcap_field_name_value
            last_record_group_list['form_date_field'] = form_date_field
            last_record_group_list['timestamp'] = timestamp
            last_record_group_list['form_completed_field_name'] = form_completed_field_name
            last_record_group_list['form_imported_field_name'] = form_imported_field_name
            
        #print redcap_field_name_value+' '+result_value
        #print last_record_group_list['form_name']
            logger.debug("generate_redcap_eav: current and last record group match: " + last_record_group +"\n"  + current_record_group)
            logger.debug("generate_redcap_eav: last_record_group_list values: " + str(last_record_group_list))

            # Append the current field name to the list of found field names
            component_list.append(redcap_field_name_value)
            
            # For datum records, output the fields
            #   Study_Id,eventName,redcapFieldNameValue,result_Value    
            eav_str = study_id + ',"' + event_name + '",' + \
                redcap_field_name_value + ',' + result_value + "\n"
            eav_file.write(eav_str.encode('utf-8'))

            # For unit records, output the fields
            #   Study_Id,eventName,redcapFieldNameUnits,Reference_Unit

            if redcap_field_name_units != "redcapFieldNameUnitsUndefined":
                eav_str = study_id + ',"' + event_name + '",' + \
                    redcap_field_name_units + ',"' + reference_unit + '"\n'
                eav_file.write(eav_str.encode('utf-8'))
    
    ''' last iteration START

    '''
    initialize_componentdict()
    #print component_list
    component_dict = rule_engine(component_list, last_record_group_list['form_name'])
    logger.debug("generate_redcap_eav: " + str(component_dict))
    if component_dict is None:
        logger.error('Returned null component dictionary')

    stat = 'YES'
    #print last_record_group_list['field_name']
    #print component_dict
    #print last_record_group_list['form_name']
    #if component_dict is not None:
    for myfield, myvalue in component_dict.iteritems():
        if myvalue is False and status_dict[myfield] is not None:
            stat = 'NOT_DONE'
            eav_str = \
            last_record_group_list['study_id'] + ',"' + \
            last_record_group_list['event_name'] + '",' + \
            str(status_dict[myfield]) +',"' +\
            stat + '"\n'
            eav_file.write(eav_str.encode('utf-8'))
    
    all_dates.add(last_record_group_list['timestamp'])
    subject_dates[study_id].append(last_record_group_list['timestamp'])
    eav_str = \
            last_record_group_list['study_id'] + ',"' + \
            last_record_group_list['event_name'] + '",' + \
            last_record_group_list['form_date_field'] + ',"' + \
            last_record_group_list['timestamp'] + '"\n'
    eav_file.write(eav_str.encode('utf-8'))

    completed_field_name = last_record_group_list['form_completed_field_name']
    if completed_field_name in form_data.values():
        total_form_counts[completed_field_name] = \
        total_form_counts[completed_field_name] + 1
        consolidated_form_data[completed_field_name][last_record_group_list['study_id']] = \
        consolidated_form_data[completed_field_name][last_record_group_list['study_id']] +1
    
    # For form completed records, output the fields
    #   Study_Id,eventName,formCompletedFieldName, 2
    eav_str = last_record_group_list['study_id'] + ',"' + \
            last_record_group_list['event_name'] + '",' + \
            last_record_group_list['form_completed_field_name'] + ',2\n'
    eav_file.write(eav_str.encode('utf-8'))

        # For form imported records, output the fields
        #   Study_Id,eventName,formImportedFieldName, yes
        #  NOT_DONE -> NO | null -> YES
    if last_record_group_list['form_imported_field_name'] != 'undefined' :
		eav_str = last_record_group_list['study_id'] + ',"' + \
				last_record_group_list['event_name'] + '",' + \
				last_record_group_list['form_imported_field_name'] + ',"Y"\n'
		eav_file.write(eav_str.encode('utf-8'))
    '''LAST ITERATION END

    '''
    date_lst = list(sorted(all_dates))
    subject_details = {}
    
    subjects = subject_dates.keys()
    import datetime
    for k in subjects:
        dates = sorted(subject_dates[k])
        if len(dates) >= 1:
            earliest_date = datetime.datetime.strptime(dates[0], output_date_format).date()
            latest_date = datetime.datetime.strptime(dates[len(dates)-1], output_date_format).date()
            delta = (latest_date - earliest_date).days
            subject_data = {}
            for form,value in form_data.items():
                s = form + "_Forms"
                subject_data[s] = consolidated_form_data[value][k]
            subject_data.update({'earliestdate':earliest_date,'latestdate':latest_date,'StudyPeriod':delta})
            subject_details[k] = subject_data
    
    for k,v in form_data.items():
        s = 'Total_'+k+'_Forms'
        report_data[s] = total_form_counts[v]
    report_data.update({'total_unique_dates':len(all_dates), 'total_subjects':len(subjects), 'cumulative_start_date':date_lst[0],
                    'cumulative_end_date':date_lst[len(date_lst)-1],'subject_details':subject_details})
    eav_file.close()
    return report_data


def init_statusdict():
    '''This function initializes status dictionary from the translationTable
    for eg., {'wbc_lborres':'wbc_lbstat',
                'neut_lborres':'neut_lbstat'}

    '''
    status_dict = {}
    for component in translational_table_tree.getroot():
        status_dict[component.findtext("redcapFieldNameValue")] = \
            component.findtext("redcapFieldNameStatus")
    return status_dict

def initialize_componentdict():
    '''This function initializes component dictionary with 'False'
        values for all the forms taken from translational_table_tree
        define the component dictionary 
        list all the components under a form and mark them as 'False' as 
        default value.
        Radha

    '''
    global component_dict
    component_dict = defaultdict(lambda: defaultdict(lambda: dict()))
    for component in translational_table_tree.getroot():
        form_name = component.findtext("redcapFormName")
        field_name = component.findtext("redcapFieldNameValue")
        component_dict[form_name][field_name] = False

def rule_engine(component_list, form_name):
    '''This function contains the component dictionary for each of the forms
        initialzed to 0's at the starting. But as each form entry comes in
        they will be populated with '1' or any non zero value.
        Finally checked for the zero values to see if the component is filled

    '''
    # if the component list is empty return
    if not component_list:
        return None
    if not form_name:
        return None
    # The program dynamically changes the value to 'True' if it 
    # encounters the value in the subject
    
    for component in component_list:
        component_dict[form_name][component] = True
        
    return component_dict[form_name]

def init_redcap_interface(setup):
    '''This function initializes the variables requrired to send data to redcap
        interface. This reads the data from the setup.json and fills the dict
        with required properties.
        Radha

    '''
    logger.info('Initializing redcap interface')
    host = ''
    path = ''

    token = setup['token']
    redcap_uri = setup['redcap_uri']

    #print str(token) + " " + str(redcap_uri)

    if redcap_uri is None:
        host = '127.0.0.1:8998'
        path = '/redcap/api/'
    if token is None:
        token = '4CE405878D219CFA5D3ADF7F9AB4E8ED'

    # parse URI to get host name only and path only
    uri_list = redcap_uri.split('//')
    #print(uri_list)
    http_str = ''
    if uri_list[0] == 'https:':
        is_secure = True
    else:
        is_secure = False
    after_httpstr_list = uri_list[1].split('/', 1)
    host = http_str + '//' + after_httpstr_list[0]
    host = after_httpstr_list[0]
    path = '/' + after_httpstr_list[1]
    properties = {'host' : host, 'path' : path, "is_secure" : is_secure,
                    'token': token}
    #print properties
    logger.info("redcap interface initialzed")
    return properties


def send_data_to_redcap(properties, data, token, format_param='csv',
        type_param='eav', overwrite_behavior='normal', return_content='ids',
        return_format='xml'):
    '''This function sends data to redcap using POST method

    '''
    logger.info('sending data to redcap')
    params = {}
    if token != '':
        params['token'] = token
    else:
        params['token'] = properties['token']
    params['content'] = 'record'
    params['format'] = format_param
    params['type'] = type_param
    params['overwriteBehavior'] = overwrite_behavior
    params['data'] = data
    params['returnContent'] = return_content
    params['returnFormat'] = return_format

    if properties['is_secure'] is True:
        redcap_connection = httplib.HTTPSConnection(properties['host'])
    else:
        redcap_connection = httplib.HTTPConnection(properties['host'])
    #print (params)
    #print self.path
    #print urlencode(params)
    logger.debug('data sent to path : %s', properties['path'])
    redcap_connection.request('POST', properties['path'], urlencode(params),
        {'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'})
    response_buffer = redcap_connection.getresponse()
    returned = response_buffer.read()
    #print(returned)
    logger.info('***********RESPONSE RECEIVED FROM REDCAP***********')
    logger.debug(returned)
    redcap_connection.close()
    return returned

def convert_clinical_data_to_xml():
    '''This function takes the file copied from the ftp server as input
        and convert it to xml data

    '''
    pass

class LogException(Exception):
    '''Class to log the exception
        logs the exception at an error level

    '''
    def __init__(self, *val):
        self.val = val

    def __str__(self):
        logger.error(self.val)
        return repr(self.val)


def configure_logging():
    '''Function to configure logging.

        The log levels are defined below. Currently the log level is
        set to DEBUG. All the logs in this level and above this level
        are displayed. Depending on the maturity of the application
        and release version these levels will be further
        narrowed down to WARNING
        

        Level       Numeric value
        =========================
        CRITICAL        50
        ERROR           40
        WARNING         30
        INFO            20
        DEBUG           10
        NOTSET          0

    '''
    # create logger
    global logger
    logger = logging.getLogger('redi')
    # configuring logger file and log format
    # setting default log level to Debug
    logging.basicConfig(filename=proj_root+'log/redi.log',
                        format='%(asctime)s - %(levelname)s - \
                        %(name)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filemode='w',
                        level=logging.DEBUG)

def send_report(sender,receiver,body):
    '''
    Function to email the report of the redi run.
    mohan
    '''
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ",".join(receiver)
    msg['Subject'] = "Data Import Report"
    msg.attach(MIMEText(body, 'html'))
    
    """
    Sending email

    """
    
    try:
       smtpObj = smtplib.SMTP('smtp.ufl.edu',25)
       smtpObj.sendmail(sender, receiver, msg.as_string())
       print "Successfully sent email"
    except Exception:
        print "Error: unable to send email"

def create_summary_report(report_parameters, report_data, form_data, alert_summary):
    from lxml import etree
    root = etree.Element("report")
    root.append(etree.Element("header"))
    root.append(etree.Element("summary"))
    root.append(etree.Element("alerts"))
    root.append(etree.Element("subjectsDetails"))
    updateReportHeader(root,report_parameters)
    updateReportSummary(root,report_data,form_data)
    updateSubjectDetails(root,report_data['subject_details'])
    updateReportAlerts(root, alert_summary)
    tree = etree.ElementTree(root)
    write_element_tree_to_file(tree, report_parameters.get('report_file_path'))
    return tree
    
def updateReportHeader(root,report_parameters):
    import time
    header = root[0]
    project = etree.SubElement(header, "project")
    project.text = report_parameters.get('project')
    date = etree.SubElement(header, "date")
    date.text = time.strftime("%m/%d/%Y")
    redcapServerAddress = etree.SubElement(header, "redcapServerAddress")
    redcapServerAddress.text = report_parameters.get('redcap_server')

def updateReportSummary(root,report_data,form_data):
    summary = root[1]
    subjectCount = etree.SubElement(summary, "subjectCount")
    subjectCount.text = str(report_data.get('total_subjects'))
    forms = etree.SubElement(summary, "forms")
    for k in sorted(form_data.keys()):
        s = 'Total_'+k+'_Forms' 
        form = etree.SubElement(forms, "form")       
        name_element = etree.SubElement(form,"form_name")
        name_element.text = s
        count_element = etree.SubElement(form,"form_count")
        count_element.text = str(report_data.get(s))
    uniqueDates = etree.SubElement(summary, "total_unique_dates")
    uniqueDates.text = str(report_data.get('total_unique_dates'))
    dates = etree.SubElement(summary, "dates")
    dates.append(etree.Element("earliestDate"))
    dates.append(etree.Element("latestDate"))
    dates[0].text = report_data.get('cumulative_start_date')
    dates[1].text = report_data.get('cumulative_end_date')

def updateReportAlerts(root, alert_summary):
    alerts = root[2]
    too_many_forms = etree.SubElement(alerts, 'tooManyForms')
    too_many_values = etree.SubElement(alerts, 'tooManyValues')
    for event in alert_summary['max_event_alert']:
        event_alert = etree.SubElement(too_many_forms, 'eventAlert')
        msg = etree.SubElement(event_alert, 'message')
        msg.text = event
    for value in alert_summary['multiple_values_alert']:
        values_alert = etree.SubElement(too_many_values, 'valuesAlert')
        msg = etree.SubElement(values_alert, 'message')
        msg.text = value

def updateSubjectDetails(root,subject_details):
    subjectsDetails = root[3]
    for key in subject_details.keys():
        subject = etree.SubElement(subjectsDetails, "Subject")
        details = subject_details.get(key)
        subjectId = etree.SubElement(subject, "ID")
        subjectId.text = key
        forms = etree.SubElement(subject, "forms")
        for k in sorted(details.keys()):
            if(k.endswith("_Forms")):
                form = etree.SubElement(forms, "form")       
                name_element = etree.SubElement(form,"form_name")
                name_element.text = k
                count_element = etree.SubElement(form,"form_count")
                count_element.text = str(details.get(k))
            else: 
                element = etree.SubElement(subject, k)
                element.text = str(details.get(k))


if __name__ == "__main__":
    main()

