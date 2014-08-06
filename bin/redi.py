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
import time
import pprint
from collections import defaultdict
from collections import Counter
import string
import httplib
import smtplib
from urllib import urlencode
import xml.etree.ElementTree as ET #Ruchi
import os
import sys
import imp
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin/utils/')
from redcap_transactions import redcap_transactions
import redi_lib


smtp_host_for_outbound_mail = None

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
    global smtp_host_for_outbound_mail
    smtp_host_for_outbound_mail = setup['smtp_host_for_outbound_mail']

    # load custom post-processing rules
    rules = load_rules(setup, proj_root)

    # read in 3 main data files / translation tables
    raw_xml_file = proj_root+ setup['raw_xml_file']
    form_events_file = proj_root+ setup['form_events_file']
    translation_table_file = proj_root+ setup['translation_table_file']
    data_file_path = proj_root+ setup['data_file_path']
    report_parameters = {'report_file_path':proj_root+setup['report_file_path'],'project':setup['project'],'redcap_server':setup['redcap_server']}
    # report_xsl = proj_root+ setup['report_xsl_path']
    report_xsl = proj_root + "bin/utils/report.xsl"
    report_file_path2 = setup['report_file_path2']
    send_email = setup['send_email']
    input_date_format = setup['input_date_format']
    output_date_format = setup['output_date_format']
    include_rule_errors_in_report = bool(setup.get('include_rule_errors_in_report', False))


    # Set path to log file
    # system_log_file = setup['system_log_file']

    # parse the raw.xml file and fill the etree rawElementTree
    data = parse_raw_xml(raw_xml_file)

    data = verify_and_correct_collection_date(data)
    # write_element_tree_to_file(data, proj_root+'raw_with_proper_dates.xml')
    # check if raw element tree is empty
    if not data:
        # raise an exception if empty
        raise LogException('data is empty')

    # add blank elements to each subject in data tree
    add_elements_to_tree(data)

    #replace fields in raw_xml
    data = replace_fields_in_raw_xml(data,setup['replace_fields_in_raw_data_xml'])

    #Convert COMPONENT_ID to loinc_code in the raw data
    component_to_loinc_code_xml = proj_root+ setup['component_to_loinc_code_xml']
    # component_to_loinc_code_xsd = proj_root+ setup['component_to_loinc_code_xsd']
    component_to_loinc_code_xsd = proj_root + "bin/utils/component_id_to_loinc_code.xsd"
    component_to_loinc_code_xml_tree = validate_xml_file_and_extract_data(component_to_loinc_code_xml,component_to_loinc_code_xsd)
    convert_component_id_to_loinc_code(data,component_to_loinc_code_xml_tree)
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

    #Create empty events for one subject and save it to the all_form_events.xml
    all_form_events_per_subject = create_empty_events_for_one_subject_helper(form_events_file,translation_table_file)
    write_element_tree_to_file(all_form_events_per_subject, proj_root+'all_form_events.xml')

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

    # components_tree = generateComponentToLoincCode2(translational_table_tree)
#     write_element_tree_to_file(components_tree, proj_root+'componentstree2.xml')

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
    update_form_imported_field(data, form_events_tree, 'undefined')
    # output raw file to check it
    write_element_tree_to_file(data, proj_root+'rawDataWithFormImported.xml')

    # update the redcapStatusFieldName
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

    properties = redcap_transactions().init_redcap_interface(setup, setup['redcap_uri'], logger)
    # Research ID - to - Redcap ID converter
    research_id_to_redcap_id_converter(data, properties, setup)

    #create person_form_event_tree.xml
    person_form_event_tree = create_empty_event_tree_for_study(data,all_form_events_per_subject)
    #write person_form_event_tree to file
    write_element_tree_to_file(person_form_event_tree, proj_root+'person_form_event_tree.xml')
    #copy data to person form event tree
    person_form_event_tree_with_data = copy_data_to_person_form_event_tree(data,person_form_event_tree,form_events_tree)
    #update status field in person form event tree
    updateStatusFieldValueInPersonFormEventTree(person_form_event_tree_with_data, translational_table_tree)
    #write person form event tree with data (both regular fields and status fields) to file
    write_element_tree_to_file(person_form_event_tree_with_data, proj_root+'person_form_event_tree_with_data.xml')

    # run custom post-processing rules
    person_form_event_tree_with_data, rule_errors = run_rules(rules, person_form_event_tree_with_data)

    # Use the new method to communicate with RedCAP
    report_data = redi_lib.generate_output(person_form_event_tree_with_data,setup)
    """
    report_data = {
        'total_subjects': 3,
        'subject_details': {
            '98':   {'Total_inr_Forms': 1, 'Total_cbc_Forms': 0},
            '99':   {'Total_inr_Forms': 1, 'Total_cbc_Forms': 1},
            '100':  {'Total_inr_Forms': 1, 'Total_cbc_Forms': 1}},
            'errors': ['RedCap Error','Test RedCap Error','Third Redcap error'],
        'form_details':
            {'Total_inr_Forms': 3, 'Total_cbc_Forms': 2}
    }
    pprint.pprint(report_data)
    """

    # Add any errors from running the rules to the report
    map(logging.warning, rule_errors)

    if include_rule_errors_in_report:
        report_data['errors'].extend(rule_errors)

    #create summary report
    xml_report_tree = create_summary_report(report_parameters, report_data, alert_summary)
    #print ElementTree.tostring(xml_report_tree)

    xslt = etree.parse(report_xsl)
    transform = etree.XSLT(xslt)
    html_report = transform(xml_report_tree)
    html_str = etree.tostring(html_report, method='html', pretty_print=True)

    # send report via email
    if send_email == 'Y':
        sender = setup["sender_email"]
        receiver = setup["receiver_email"]
        send_report(sender,receiver,html_str)
    else:
        try:
            report_file = open(report_file_path2, 'w')
        except IOError:
            raise LogException('could not open '+report_file_path2 +' file not found')
        report_file.write(html_str)

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

'''
Parse the form_events file into an ElementTree

@arg form_events_file: the name of the input file (from the json configuration)
@return ElementTree
'''
def parse_form_events(form_events_file):
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

'''
Parse the translationTable.xml into an ElementTree

@arg translation_table_file: the name of the input file
@return ElementTree
'''
def parse_translation_table(translation_table_file):
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


'''
Add blank elements to fill out in ElementTree.

@arg data: the input ElementTree from the parsed raw XML file.

Add element to data ElementTree for timestamp, redcap form name, eventName,
formDateField, and formCompletedFieldName.
'''
def add_elements_to_tree(data):
    for element in data.iter('subject'):
        element.append(etree.Element("timestamp"))
        element.append(etree.Element("redcapFormName"))
        element.append(etree.Element("eventName"))
        element.append(etree.Element("formDateField"))
        element.append(etree.Element("formCompletedFieldName"))
        element.append(etree.Element("formImportedFieldName"))
        element.append(etree.Element("redcapFieldNameValue"))
        element.append(etree.Element("redcapFieldNameUnits"))
        element.append(etree.Element("redcapStatusFieldName"))


'''
Update the redcapStatusFieldName value to all subjects
'''
def update_recap_form_status(data, lookup_data, undefined):
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapStatusFieldName'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapStatusFieldName'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

'''
Update the formImportedFieldName value for all subjects
'''
def update_form_imported_field(data, lookup_data, undefined):
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'formImportedFieldName'
    index_element_in_data = 'redcapFormName'
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    value_in_lookup_data = 'formImportedFieldName'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

'''
Write an ElementTree to a file whose name is provided as an argument
'''
def write_element_tree_to_file(element_tree, file_name):
    logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(file_name, encoding="us-ascii", xml_declaration=True, method="xml", pretty_print=True)

'''
Update timestamp using input and output data formats
reads from raw ElementTree and writes to it
'''
def update_time_stamp(data, input_date_format, output_date_format):
    logger.info('Updating timestamp to ElementTree')
    for subject in data.iter('subject'):
        # New EMR field SPECIMN_TAKEN_TIME is used in place of Collection Date and Collection Time
        specimn_taken_time = subject.find('DATE_TIME_STAMP').text

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

'''
Lookup component ID in translationTable to get the redcapFormName.
Write the redcapForm name to data
If component lookup fails, sets formName to undefinedForm
'''
def update_redcap_form(data, lookup_data, undefined):
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapFormName'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
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
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapFieldNameValue'

    update_data_from_lookup(data, element_to_set_in_data,
        index_element_in_data, lookup_data, element_to_find_in_lookup_data,
        index_element_in_lookup_data, value_in_lookup_data, undefined)

    # set redcapFieldNameUnits
    element_to_set_in_data = 'redcapFieldNameUnits'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
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
            lookup_table[child.findtext(index_element_in_lookup_data)] = \
                            child_lookup_data.text
    # Update the field value using the lookup_table we just created
    data_root = data.getroot()
    count =0
    for child in data_root:
        # get the element text, but set a default value of undefined for
        # each look up failure
        new_element_text = \
            lookup_table.get(child.findtext(index_element_in_data), undefined)
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

def research_id_to_redcap_id_converter(data, properties, setup):
  '''This function converts the research_id to redcap_id
   1. prepare a dictionary with [key, value] --> [study_id, redcap_id]
   2. replace the element tree study_id with the new redcap_id's
   for each bad id, log it as warn

  '''
  # read each of the study_id's from the data etree
  study_id_recap_id_dict = {}

  ''' Configuration data from the mapping xml

  '''
  mapping_xml = proj_root+setup['research_id_to_redcap_id']

  # read the field names from the research_id_to_redcap_id_map.xml
  # check for file existance
  if not os.path.exists(mapping_xml):
      raise LogException("Error: research id to redcap id fieldname xml not found at "
          +mapping_xml)

  mapping_data = etree.parse(mapping_xml)
  redcap_id_field_name = mapping_data.getroot().findtext('redcap_id_field_name')
  research_id_field_name = mapping_data.getroot().findtext('research_id_field_name')

  if research_id_field_name is None or research_id_field_name == '':
    logger.error('research_id_field_name tag in file %s is not present', mapping_xml)
    raise LogException('research_id_field_name tag in file %s is not present', mapping_xml)

  if redcap_id_field_name is None or redcap_id_field_name == '':
    logger.error('redcap_id_field_name tag in file %s is not present', mapping_xml)
    raise LogException('redcap_id_field_name tag in file %s is not present', mapping_xml)

  ''' Communication with redcap

  '''
  redcap_transaction = redcap_transactions()
  # query the redcap for the response with redcap id's
  properties['fields'] = research_id_field_name+','+redcap_id_field_name
  response = redcap_transaction.get_data_from_redcap(properties, properties['token'],logger,
          'Redcap', format_param='xml', type_param='flat', return_format='xml')

  import xml.etree.ElementTree as ET
  items = ET.fromstring(response)
  redcap_dict = {}
  # list of bad research ids that are not present in redcap list
  bad_ids = defaultdict(int)

  for item in items.findall('./item'):
    research_id = item.findtext(research_id_field_name)
    redcap_id = item.findtext(redcap_id_field_name)
    if research_id is not None and research_id != '':
      redcap_dict[research_id] = redcap_id

  for subject in data.iter('subject'):
      study_id = subject.findtext('STUDY_ID')
      # tag = subject.find('STUDY_ID')
      # if the study id is not null populate the dictionary
      if study_id is not None and study_id != '' and study_id in redcap_dict:
        # if the study_id in redcap_dict of redcap id's update the study_id
        # with redcap id
        subject.find('STUDY_ID').text = redcap_dict[study_id]
      elif study_id is not None and study_id != '' and study_id not in redcap_dict:
        # add the bad research id to list of bad ids
        bad_ids[study_id] += 1
        data.getroot().remove(subject)
      else:
        logger.error('Error: research id to redcap id: study_id is invalid')

  for bad_id in bad_ids.iteritems():
    logger.warn('Bad research id %s found %s times', bad_id[0], bad_id[1])

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

'''
Function to email the report of the redi run.
'''
def send_report(sender,receiver,body):
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
       smtpObj = smtplib.SMTP(smtp_host_for_outbound_mail, 25)
       smtpObj.sendmail(sender, receiver, msg.as_string())
       print "Successfully sent email to: " + str(receiver)
    except Exception:
        print "Error: unable to send report email to: " + str(receiver)


def create_summary_report(report_parameters, report_data, alert_summary):
    root = etree.Element("report")
    root.append(etree.Element("header"))
    root.append(etree.Element("summary"))
    root.append(etree.Element("alerts"))
    root.append(etree.Element("subjectsDetails"))
    root.append(etree.Element("errors"))
    updateReportHeader(root,report_parameters)
    updateReportSummary(root,report_data)
    updateSubjectDetails(root,report_data['subject_details'])
    updateReportAlerts(root, alert_summary)
    updateReportErrors(root,report_data['errors'])
    tree = etree.ElementTree(root)
    write_element_tree_to_file(tree, report_parameters.get('report_file_path'))
    return tree

def updateReportHeader(root,report_parameters):
    header = root[0]
    project = etree.SubElement(header, "project")
    project.text = report_parameters.get('project')
    date = etree.SubElement(header, "date")
    date.text = time.strftime("%m/%d/%Y")
    redcapServerAddress = etree.SubElement(header, "redcapServerAddress")
    redcapServerAddress.text = report_parameters.get('redcap_server')

def updateReportSummary(root,report_data):
    summary = root[1]
    subjectCount = etree.SubElement(summary, "subjectCount")
    subjectCount.text = str(report_data.get('total_subjects'))
    forms = etree.SubElement(summary, "forms")
    form_data = report_data['form_details']
    for k in sorted(form_data.keys()):
        form = etree.SubElement(forms, "form")
        name_element = etree.SubElement(form,"form_name")
        name_element.text = k
        count_element = etree.SubElement(form,"form_count")
        count_element.text = str(form_data.get(k))

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
    for key in sorted(subject_details.keys()):
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

def updateReportErrors(root,errors):
    errorsRoot = root[4]
    for error in errors:
        errorElement = etree.SubElement(errorsRoot, "error")
        errorElement.text = str(error)

"""
create_empty_events_for_one_subject_helper:
This function creates new copies of the form_events_tree and translation_table_tree and calls create_empty_events_for_one_subject
Parameters:
    form_events_file: This parameter holds the path of form_events file
    translation_table_file: This parameter holds the path of translation_table file

"""
def create_empty_events_for_one_subject_helper(form_events_file,translation_table_file):
    form_events_tree = parse_form_events(form_events_file)
    translation_table_tree = parse_translation_table(translation_table_file)
    return create_empty_events_for_one_subject(form_events_tree,translation_table_tree)

"""
create_empty_events_for_one_subject:
This function uses form_events_tree and translation_table_tree and creates an all_form_events_tree
Parameters:
    form_events_tree: This parameter holds form events tree
    translation_table_tree: This parameter holds translation table tree

"""
def create_empty_events_for_one_subject(form_events_tree,translation_table_tree):
        logger.info('Creating all form events template for one subject')
        from lxml import etree
        root = etree.Element("all_form_events")
        form_event_root = form_events_tree.getroot()
        translation_table_root = translation_table_tree.getroot()
        if translation_table_root is None:
            raise LogException('translation table tree is empty')
        if form_event_root is None:
            raise LogException('Form Events tree is empty')

        translation_table_dict = {}

        for component in translation_table_root.iter('clinicalComponent'):
            translation_table_dict[component.find('redcapFormName').text] = set()

        for component in translation_table_root.iter('clinicalComponent'):
            form_name = component.find('redcapFormName').text
            if component.find('redcapFieldNameValue') is not None:
                translation_table_dict[form_name].add(component.find('redcapFieldNameValue').text)
            if component.find('redcapFieldNameUnits') is not None:
                translation_table_dict[form_name].add(component.find('redcapFieldNameUnits').text)
            if component.find('redcapStatusFieldName') is not None:
                translation_table_dict[form_name].add(component.find('redcapStatusFieldName').text)

        for form in form_event_root.iter('form'):
            for child in form:
                form_child = child.tag
                if form_child.startswith("form"):
                    try:
                        if form_child != 'formCompletedFieldValue' and form_child != 'formImportedFieldValue':
                            translation_table_dict[form.find('name').text].add(child.text)
                    except KeyError, e:
                        translation_table_dict[form.find('name').text] = set()
                        translation_table_dict[form.find('name').text].add(child.text)
                    form.remove(child)
            all_fields = etree.Element("allfields")
            try:
                for field in translation_table_dict[form.find('name').text]:
                    field_tag = etree.SubElement(all_fields, "field")
                    name = etree.SubElement(field_tag, "name")
                    name.text = field
                    value = etree.SubElement(field_tag, "value")
            except KeyError,e:
                raise LogException('There are no fields in this form.')

            for child in form.iter('event'):
                child.insert(child.index(child.find('name'))+1,
                etree.XML(etree.tostring(all_fields, method='html', pretty_print=True)))
            etree.strip_tags(form,'allfields')

            root.append(form)
        tree = etree.ElementTree(root)
        return tree

"""
create_empty_event_tree_for_study:
This function uses raw_data_tree and all_form_events_tree and creates a person_form_event_tree for study
Parameters:
    raw_data_tree: This parameter holds raw data tree
    all_form_events_tree: This parameter holds all form events tree

"""
def create_empty_event_tree_for_study(raw_data_tree, all_form_events_tree):
    logger.info('Creating all form events template for all subjects')
    from lxml import etree
    root = etree.Element("person_form_event")
    raw_data_root = raw_data_tree.getroot()
    all_form_events_root = all_form_events_tree.getroot()
    if raw_data_root is None:
        raise LogException('Raw data tree is empty')
    if all_form_events_root is None:
        raise LogException('All form Events tree is empty')

    subjects_list = set()

    for subject in raw_data_root.iter('subject'):
        subjects_list.add(subject.find('STUDY_ID').text)

    if not subjects_list:
        raise LogException('There is no subjects in the raw data')

    for subject_id in subjects_list:
        person = etree.Element("person")
        study_id = etree.SubElement(person, "study_id")
        study_id.text = subject_id
        person.insert(person.index(person.find('study_id'))+1,
        etree.XML(etree.tostring(all_form_events_root, method='html', pretty_print=True)))
        root.append(person)

    tree = etree.ElementTree(root)
    return tree

def setStat(event, translation_table_dict, translation_table_status_field_text_list):
  """
  Ruchi Vivek Desai, May 13 2014
  to assist the updateStatusFieldValueInPersonFormEventTree function
  """
  #iterates over all fields under event (passed as parameter) in source file
  for field in event.iter('field'): #loop3
    value = field.find('value')
    if (value is not None and value.text is not None):
      logger.info("text is missing")
      continue

    name = field.find('name')
    if (name is None):
      logger.info("tag is missing")
      continue

    is_status_field = name.text in translation_table_status_field_text_list
    if (is_status_field):
      logger.info("This tag needs to be skipped as it might stand for status")
      continue

    doesnt_have_status_field = name.text not in translation_table_dict or translation_table_dict[name.text][0] == ""
    if (doesnt_have_status_field):
      logger.info("This tag needs to be skipped as it might stand for form name")
      continue #name could have been a redcap form name like cbc_lbdtc

    set_status_for(name, event, translation_table_dict)

def set_status_for(field_name, event, translation_table_dict):
  """
  Ruchi
  """
  for field in event.iter('field'):
    name = field.findtext('name', "")
    if (name == translation_table_dict[field_name.text][0]):
      value = field.find('value')
      value.text = translation_table_dict[field_name.text][1]
      return

def updateStatusFieldValueInPersonFormEventTree(person_form_event_tree, translational_table_tree):
  """
  Ruchi Vivek Desai, May 13 2014
  This function updates the status field value with either NOT_DONE (value in the translation table)
  or empty string based on certain conditions
  """
  # Get root of peron form event tree
  person_form_event__tree_root = person_form_event_tree.getroot()
  if (person_form_event__tree_root is None):
    # Log error: Person Form Event Tree is empty
    raise LogException('Person Form Event Tree is empty')

  else:
    # Get root of translation table
    translation_table_root = translational_table_tree.getroot()
    if (translation_table_root is None):
      # Log error: Translation Table Tree is empty
      raise LogException("Translation Table Tree is empty")
    else:
      # This list contains text values of redcapStatusFieldName, to avoid searching for elements with this text later in setStat function
      translation_table_status_field_text_list = [x.text for x in translation_table_root.iter('redcapStatusFieldName') if x.text is not None]
      # Parse translation table and make a dictionary to store the person form event tree fields along with their respective status field info
      translation_table_dict = {}
      for clinical_component in translation_table_root:
        if (clinical_component is None):
          continue
        else:
          redcap_status_field_name = clinical_component.findtext("redcapStatusFieldName", "")
          redcap_status_field_value = clinical_component.findtext("redcapStatusFieldValue", "")

          # For every redcap_field other than redcapStatusFieldName and redcapStatusFieldValue in this clinical_component add an entry, {redcap_field.text: [redcapStatusFieldName, redcapStatusFieldValue]} to translation_table_dict
          for redcap_field in clinical_component:
            if (redcap_field is None):
              continue
            elif (redcap_field.tag == "redcapFormName" or redcap_field.tag == "redcapStatusFieldName" or redcap_field.tag == "redcapStatusFieldValue"):
              continue
            elif (redcap_field.text in translation_table_dict):
              continue
            else:
              translation_table_dict[redcap_field.text] = [redcap_status_field_name, redcap_status_field_value]
          #End of for redcap_field in clinical_component:
      #End of for clinical_component in translation_table_root:
    #At this point we have the dictionary for the translation table ready

    #For every event in person form event tree, get the text of 'value', which is a descendant of event (child of field), and add it to field_values
    #This checks if the event is completely blank or has some values. We need to update the status field only if the event has some values
    for event in person_form_event__tree_root.iter('event'):
      field_values = ""
      if (event is None):
        continue
      else:
        for value in event.iter('value'):
          if(value is None):
            continue
          elif (str(value.text) == "None"):
            field_values += ""
          else:
            field_values += value.text
        #End of for value in event.iter('value'):
        if (field_values == ""):
          logger.info("Empty event")
          continue
        else:
          setStat(event, translation_table_dict, translation_table_status_field_text_list)

    #Write the modified tree to an xml file as output
    #person_form_event_tree.write("op1.xml")

"""
copy_data_to_person_form_event_tree:
This function copies data from the raw_data_tree to the person_form_event_tree
Parameters:
    raw_data_tree: This parameter holds raw data tree
    person_form_event_tree: This parameter holds person form event tree
    form_events_tree: This parameter holds form events tree

"""
def copy_data_to_person_form_event_tree(raw_data_tree,person_form_event_tree,form_events_tree):
    logger.info('Copying data to person form event tree')
    raw_data_root = raw_data_tree.getroot()
    person_form_event_tree_root = person_form_event_tree.getroot()
    form_event_root = form_events_tree.getroot()
    if raw_data_root is None:
        raise LogException('Raw data tree is empty')
    if person_form_event_tree_root is None:
        raise LogException('Person Form Event tree is empty')
    if form_event_root is None:
        raise LogException('Form Events tree is empty')

    for subject in raw_data_root.iter('subject'):
        eventName = subject.find("eventName").text
        if eventName:
           study_id_object = subject.find("STUDY_ID")
           formNameObject = subject.find("redcapFormName")
           fieldNameObject = subject.find("redcapFieldNameValue")
           fieldValueObject = subject.find("RESULT")
           dateFieldObject = subject.find("formDateField")
           dateValueObject = subject.find("timestamp")
           fieldUnitsNameObject = subject.find("redcapFieldNameUnits")
           fieldUnitsValueObject = subject.find("REFERENCE_UNIT")
           formCompletedField = subject.find("formCompletedFieldName")
           formImportedField = subject.find("formImportedFieldName")


           logger.info('Checking for required fields')
           if study_id_object is None:
               raise LogException('Missing required field STUDY_ID')
           else:
               subject_id = study_id_object.text


           if formNameObject is None:
               raise LogException('Missing required field redcapFormName')
           else:
               formName = formNameObject.text
               if formName == 'undefined':
                   continue


           if fieldNameObject is None:
               raise LogException('Missing required field redcapFieldNameValue')
           else:
               redcapFieldName = fieldNameObject.text


           if fieldValueObject is None:
               raise LogException('Missing required field RESULT')
           else:
               redcapFieldValue = fieldValueObject.text

           if dateFieldObject is None:
               raise LogException('Missing required field formDateField')
           else:
               dateField = dateFieldObject.text

           if dateValueObject is None:
               raise LogException('Missing required field timestamp')
           else:
               dateValue = dateValueObject.text

           if fieldUnitsNameObject is None:
               raise LogException('Missing required field redcapFieldNameUnits')
           else:
               redcapFieldUnitsName = fieldUnitsNameObject.text

           if fieldUnitsValueObject is None:
               raise LogException('Missing required field REFERENCE_UNIT')
           else:
               redcapFieldUnitsValue = fieldUnitsValueObject.text

           form = person_form_event_tree_root.xpath("person/study_id[.='"+subject_id+"']/../all_form_events/form/name[.='"+formName+"']")

           if len(form)<1:
                raise LogException('Form named '+formName+' Not Found in person form event tree for subject '+subject_id)

           logger.info('Check passed. Copying data with subject_id:' + subject_id \
            + ", formName:" +formName\
            + ", eventName:" +eventName \
            + ", dateValue:" +dateValue \
            + ", redcapFieldName:" +redcapFieldName \
            + ", redcapFieldUnitsName:" +redcapFieldUnitsName \
            )

           # Copy the first three data fields into the PFE Tree
           path = "person/study_id[.='"+subject_id+"']/../all_form_events/form/name[.='"+formName+"']/../event/name[.='"+eventName+"']/../field"
           fields = person_form_event_tree_root.xpath(path)
           fieldValues = ""
           for node in fields:
               if node.find("name").text == redcapFieldName:
                   node.find("value").text = redcapFieldValue
                   fieldValues = fieldValues + convert_none_type_object_to_empty_string(redcapFieldValue)
                   continue
               if node.find("name").text == dateField:
                   node.find("value").text = dateValue
                   fieldValues = fieldValues + convert_none_type_object_to_empty_string(dateValue)
                   continue
               if node.find("name").text == redcapFieldUnitsName:
                   node.find("value").text = redcapFieldUnitsValue
                   fieldValues = fieldValues + convert_none_type_object_to_empty_string(redcapFieldUnitsValue)
                   continue

           # If we had values in any of the first three fields, copy the form_completed and imported fields
           if fieldValues:
              completedFieldValue = person_form_event_tree_root.xpath("person/study_id[.='"+subject_id+"']/../all_form_events/form/name[.='"+formName+"']/../event/name[.='"+eventName+"']/../field/name[.='"+formCompletedField.text+"']/../value")
              completedFieldValue[0].text = form_event_root.xpath("form/name[.='"+formName+"']/../formCompletedFieldValue")[0].text
              importedFieldValue = person_form_event_tree_root.xpath("person/study_id[.='"+subject_id+"']/../all_form_events/form/name[.='"+formName+"']/../event/name[.='"+eventName+"']/../field/name[.='"+formImportedField.text+"']/../value")
              importedFieldValue[0].text = form_event_root.xpath("form/name[.='"+formName+"']/../formImportedFieldValue")[0].text

              if not completedFieldValue[0].text:
                  raise LogException('formCompletedField not set properly in the person form event tree')
              if not importedFieldValue[0].text:
                  raise LogException('formImportedField not set properly in the person form event tree')

    tree = etree.ElementTree(person_form_event_tree_root)
    return tree

"""
replace noneType objects with an empty string. Else return the object.
"""
def convert_none_type_object_to_empty_string(my_object):
    return ('' if my_object is None else my_object)

"""
convert_component_id_to_loinc_code:
This function converts COMPONENT_ID in raw data to loinc_code based on the mapping provided in the xml file
Parameters:
    data: Raw data xml tree
    component_to_loinc_code_xml_tree: COMPONENT_ID to loinc_code mapping xml file tree.

"""
def convert_component_id_to_loinc_code(data, component_to_loinc_code_xml_tree):
    component2loinc_root = component_to_loinc_code_xml_tree.getroot()
    if component2loinc_root is None:
        raise LogException('component_to_loinc_code_xml is empty')

    for component in component2loinc_root.iter('component'):
        source_name = component.findtext('source/name')
        source_value = component.findtext('source/value')
        target_name = component.findtext('target/name')
        target_value = component.findtext('target/value')
        if source_name and source_value and target_name:
            path = "subject/"+source_name+"[.='"+source_value+"']/.."
            subjects_to_change = data.xpath(path)
            if len(subjects_to_change)<1:
                logger.debug('There are no matching sujects to modify in the Raw Data')
            for subject in subjects_to_change:
                new_target_element = etree.Element(target_name)
                new_target_element.text = target_value
                source_element = subject.find(source_name)
                subject.replace(source_element,new_target_element)
        else:
            raise LogException("Elements source/name and Source/value are not present in the component_to_loinc_code xml")
    return data

"""
validate_xml_file_and_extract_data:
This function is responsible for validating xml file against an xsd and to extract data from xml if validation succeeds
Parameters:
    xmlfilename: This parameter holds the path to the xml file
    xsdfilename: This parameter holds the path to the xsd file

"""
def validate_xml_file_and_extract_data(xmlfilename,xsdfilename):
    if not os.path.exists(xsdfilename):
        raise LogException("Error: "+xsdfilename+" xsd file not found at "
            + xsdfilename)
    else:
        xsdfilehandle = open(xsdfilename, 'r')
        logger.info(xmlfilename+" Xsd file read in. ")

    xsd_tree = etree.parse(xsdfilename)
    xsd = etree.XMLSchema(xsd_tree)

    if not os.path.exists(xmlfilename):
        raise LogException("Error: "+xmlfilename+" xml file not found at "
            + xmlfilename)
    else:
        xmlfilehandle = open(xmlfilename, 'r')
        logger.info(xmlfilename+" XML file read in. " +  str(sum(1 for line in xmlfilehandle))
            + " total lines in file.")
    xml = etree.parse(xmlfilename)
    if not xsd.validate(xml):
        raise LogException("XSD Validation Failed for xml file %s and xsd file %s",xmlfilename,xsdfilename)
    return xml

"""
replace_fields_in_raw_xml:
This function renames all fields which need renaming.Fields which need renaming are read from the xml file.
Parameters:
    data: Raw data xml tree
    fields_to_replace_xml: Path to xml file which has list of fields which need renaming.

"""
def replace_fields_in_raw_xml(data,fields_to_replace_xml):
    file_path = proj_root+fields_to_replace_xml
    if not os.path.exists(file_path):
        raise LogException("Error: "+fields_to_replace_xml+" xml file not found at "
            + fields_to_replace_xml)
    else:
        fields_to_replace_xml_handle = open(file_path, 'r')
        logger.info(fields_to_replace_xml+" Xml file read in. ")

    fields_to_replace_xml_tree = etree.parse(file_path)
    fields_to_replace_xml_tree_root = fields_to_replace_xml_tree.getroot()
    if fields_to_replace_xml_tree_root is None:
        raise LogException('replace_fields_in_raw_data.xml is empty')

    for field in fields_to_replace_xml_tree_root.iter('field'):
        source = field.findtext('source')
        target = field.findtext('target')
        for subject in data.iter('subject'):
            source_element = subject.find(source)
            if source_element is not None:
                new_target_element = etree.Element(target)
                new_target_element.text = source_element.text
                subject.replace(source_element,new_target_element)
    return data


def load_rules(setup, root='./'):
    """ Loads custom post-processing rules.

    Rules should be added to the configuration file under a property called
    "rules", which has key-value pairs mapping a unique rule name to a Python
    file. Each Python file intended to be used as a rules file should have a
    run_rules() function which takes one argument.

    Example config.json:
      { "rules": { "my_rules": "rules/my_rules.py" } }

    Example rules file:
      def run_rules(data):
        pass
    """
    if 'rules' not in setup:
        return {}

    loaded_rules = {}
    for (rule, path) in setup['rules'].iteritems():
        module = None
        if os.path.exists(path):
            module = imp.load_source(rule, path)
        elif os.path.exists(root + path):
            module = imp.load_source(rule, root + path)

        assert module is not None
        assert module.run_rules is not None

        loaded_rules[rule] = module

    return loaded_rules


def run_rules(rules, person_form_event_tree_with_data):
    errors = []

    for (rule, module) in rules.iteritems():
        try:
            module.run_rules(person_form_event_tree_with_data)
        except Exception as e:
            message_format = 'Error processing rule "{0}". {1}'
            if not hasattr(e, 'errors'):
                errors.append(message_format.format(rule, e.message))
                continue
            for error in e.errors:
                errors.append(message_format.format(rule, error))

    return person_form_event_tree_with_data, errors

def verify_and_correct_collection_date(data):
    for subject in data.iter('subject'):
        collection_date_element = subject.find('DATE_TIME_STAMP')
        result_date_element = subject.find('RESULT_DATE')
        if collection_date_element is not None and result_date_element is not None:
            if not collection_date_element.text:
                collection_date_element.text = result_date_element.text
        elif collection_date_element is None and result_date_element is not None:
            new_collection_date_element = etree.Element('DATE_TIME_STAMP')
            new_collection_date_element.text = result_date_element.text
            subject.replace(result_date_element, new_collection_date_element)
            continue
        else:
            continue
        subject.remove(result_date_element)
    return data

if __name__ == "__main__":
    main()
