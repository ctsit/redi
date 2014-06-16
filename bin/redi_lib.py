#/usr/bin/env python

"""
redi_lib.py

    Stores a collection of utility functions used by redi.py
"""

__author__      = "Andrei Sura"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 2-Clause"
__version__     = "0.1"
__email__       = "asura@ufl.edu"
__status__      = "Development"


from lxml import etree
import logging
import pprint
from collections import defaultdict
from collections import Counter
import string
import datetime
import httplib
from urllib import urlencode
import os
import sys
from redcap_transactions import redcap_transactions

import xml.etree.ElementTree as ET
import redi
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin/utils/')

"""
=============================================
=== create_eav_output
@return dictionary(
    'csv' : ...
    'contains_data': ...
    )

Helper function for transforming the fragment:
<event>
    <name>1_arm_1</name>
    <field>
        <name>chem_lbdtc</name>   <!-- valid text -->
        <value>1902-12-17</value>
    </field>
    <field> ...

into

record,redcap_event_name,field_name,value
73,"1_arm_1",chem_lbdtc,"1902-12-17"
73,"1_arm_1",chem_complete,"2"
...
"""
def create_eav_output(study_id, event_tree):
    redi.configure_logging()

    if (not study_id):
        raise redi.LogException('Expected a valid value for study_id')

    root = event_tree
    if (root is None or not root.findall('*')) :
        # Covers the case when the input is empty string or just "<event></event>"
        return ''

    event_field_value_list = root.xpath('//event/field/name')
    for name in event_field_value_list : 
        if name.text is None :
            raise redi.LogException('Expected non-blank element event/field/name')

    # Each row has a prefix composed of study_id and event name:
    # 3,"1_arm_1",
    event_name = root.find('name')
    if event_name is None:
        raise redi.LogException('Expected non-blank element event/name')

    header = '\nrecord,redcap_event_name,field_name,value'
    result_csv = header
    row_prefix = str(study_id) + ',"' + event_name.text + '"'

    # Match all fields to build a row for each
    event_field_list = root.xpath('field')
    contains_data = False

    for field in event_field_list :
        val = get_child_text_safely(field, 'value')
        result_csv += '\n' + row_prefix +  ',' + field.find('name').text
        result_csv += ',"' + val + '"'

        if val and not contains_data:
            contains_data = True

    return {'csv' : result_csv, 'contains_data' : contains_data}

"""
Convenience function
@see create_eav_output
"""
def get_child_text_safely(etree, ele) :
    ele = etree.find(ele)
    if ele.text is None:
        return ''
    else :
        return ele.text

"""
=============================================
=== generate_output
Note: This function communicates with the redcap application.
Steps:
    - loop for each person/form/event element
    - generate a csv fragment `using create_eav_output`
    - send csv fragment to RedCap using `send_eav_data_to_redcap`


@return the report_data dictionary 
"""
def generate_output(person_tree) :
    redi.configure_logging()

    # the global dictionary to be returned
    report_data = { 
        'errors' : [] 
    }

    """
     For each person we keep a count for each form type:
        subject_details = array(
            'person_A' => array('form_1': 1, 'form_2': 10, ...
            'person_B' => array('form_1': 1, 'form_2': 10, ...
            ...
        )
    """ 
    subject_details = {}

    # For each form type we keep a global count
    form_details = {}

    # count how many `person` elements are parsed
    person_count = 0

    # count how many csv fragments are created
    event_count = 0

    root = person_tree.getroot()
    persons = root.xpath('//person')
    setup_json = proj_root+'config/setup.json'
    setup = redi.read_config(setup_json)
    
    redcapTransactionsObject = redcap_transactions()
    properties = redcapTransactionsObject.init_redcap_interface(setup, setup['redcap_uri'], redi.logger)
    redcap_connection = redcapTransactionsObject.get_redcap_connection(properties, setup['token'])
   
    # main loop for each person
    for person in persons :
        time_begin = datetime.datetime.now()
        person_count += 1
        study_id = (person.xpath('study_id') or [None])[0]

        if study_id is None:
            raise redi.LogException('Expected a valid value for study_id')

        forms = person.xpath('./all_form_events/form')

        # loop through the forms of one person
        for form in forms:
            form_name = form.xpath('name')[0].text
            form_key =  'Total_'+form_name+'_Forms'
            study_id_key = study_id.text

            # init dictionary for a new person in (study_id)
            if not study_id_key in subject_details:
                subject_details[study_id_key] = {}

            if not form_key in subject_details[study_id_key] :
                subject_details[study_id_key][form_key] = 0

            if not form_key in form_details :
                form_details[form_key] = 0

            redi.logger.debug('parsing study_id ' + study_id.text + ' form: ' + form_name)
            
            # loop through the events of one form
            for event in form.xpath('event') :
                event_count += 1

                try :
                    #print etree.tostring(event)
                    csv_dict = create_eav_output(study_id.text, event)
                    eav_string = csv_dict['csv']
                    contains_data = csv_dict['contains_data']

                    #redi.logger.debug('Created eav string: \n' + eav_string)
                    #print ('Created eav string: \n' + eav_string)

                    #time_begin_send = datetime.datetime.now()
                    response = redcapTransactionsObject.send_data(redcap_connection, properties, eav_string, redi.logger)
                    #time_end_send = datetime.datetime.now()
                    #redi.logger.debug("Execution time for `send_data` was: " + str(time_end_send - time_begin_send))

                    #response = send_eav_csv_data_to_redcap(eav_string)
                    #redi.logger.debug('RedCAP response xml: ' + response)
                    found_error = handle_errors_in_redcap_xml_response(response,report_data)

                    if not found_error and contains_data :
                        # if no errors encountered update event counters
                        subject_details[study_id_key][form_key] += 1
                        form_details[form_key] += 1
                    
                except Exception:
                    redi.logger.error( "Problem detected with `create_eav_output` or `send_data_to_redcap`")
                    raise
                    continue

        time_end = datetime.datetime.now()
        print "Total execution time for study_id %s was %s" % (study_id_key, (time_end - time_begin))

    #pprint.pprint(subject_details)
    # total_unique_dates = root.xpath('count(//form/event/)')

    report_data.update({
        'total_subjects'        :   person_count,
        'form_details'          :   form_details,
        'subject_details'       :   subject_details,
        'errors'                :   report_data['errors']
    })

    redi.logger.debug('report_data ' + `report_data`)
    return report_data 

"""
handle_errors_in_redcap_xml_response:
This function checks for any errors in the redcap response and update report data if there are any errors.
Parameters:
    redcap_response_xml: This parameter holds the redcap response passed to this function
    report_data: This parameter holds the report data passed to this function
    
"""
def handle_errors_in_redcap_xml_response(redcap_response_xml, report_data):
    redi.logger.info('handling response from the REDCap')
    responseTree = ET.fromstring(redcap_response_xml)
    errorsPresent = False
    errors = responseTree.findall('error')
    if len(errors)>0:
        for error in errors:
            try:
                report_data['errors'].append(error.text)
            except KeyError,e:
                raise redi.LogException('There is no key "errors" in the report_data')
            errorsPresent = True
            
    return errorsPresent

def send_eav_csv_data_to_redcap(eav_string):
    xml = '''
<ids>
    <id>1</id>
    <id>2</id>
</ids>
'''
    return xml 


# Convenience method for getting the first element
# Note: for printing an object can use: print  repr(obj)
def get_first_item(aList) :
    if aList:
        return aList[0]
    return None


if __name__ == "__main__":
    main()
