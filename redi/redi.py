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
# Kevin Hanson <hansonks@gmail.com>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see
# http://opensource.org/licenses/BSD-3-Clause

"""
redi.py - Converter from raw clinical data in XML format to REDCap API data

Usage:
    redi.py -h | --help
    redi.py [-v] [-V] [-k] [-e] [-d] [-f=<path>] [-r] [-c=<path>] [-D=<datadir>] [-s] [-b] [-K]

Options:
    -h --help                   Show this help message and exit
    -v --verbose                Increase output verbosity [default:False]
    -V --version                Show version number [default:False]
    -k --keep                   Use this option to preserve the files
                                generated during execution [default:False]
    -e --emrdata                Use this option to get EMR data [default:False]
    -d --dryrun                 To execute redi.py in dry run state. This
                                is to be able to test each release by doing
                                a dry run, where the data is fetched and
                                processed but not transferred to the
                                production REDCap. Email is also not sent.
                                The processed data is stored as output
                                files under the "out" folder under project
                                root [default:False].
    -f --file=<filename>        Specify the path and filename to use as input for REDI.
    -r --resume                 WARNING!!! Resumes the last run. This
                                switch is for a specific case. Check the
                                documentation before using it. [default:False]
    -c --config-path=<path>     Specify the path to the configuration directory
    -D --datadir=<datadir>      Specify the path to the directory containing
                                project specific input and output data which
                                will help in running multiple simultaneous
                                instances of redi for different projects
    -s --skip-blanks            Skip blank events when sending data to REDCap
                                [default:False]
    -b --bulk-send-blanks       Send blank events in bulk instead of
                                individually [default:False]
    -K --keep-all               Keep all results, do not compress by date
"""
__author__ = "University of Florida CTS-IT Team"
__email__ = "ctsit@ctsi.ufl.edu"
__status__ = "Development"

import ast
import errno
import logging
from logging.handlers import TimedRotatingFileHandler
import math
import pickle
import time
from datetime import date, datetime, timedelta
from collections import defaultdict
from collections import Counter
import string
import xml.etree.ElementTree as ET
import sys
import imp
import os
import pkg_resources
import shutil
from pprint import pprint

from requests import RequestException
from lxml import etree
from docopt import docopt

import batch
import upload
import report
from utils import redi_email
from utils.redcapClient import RedcapClient
import utils.SimpleConfigParser as SimpleConfigParser
import utils.GetEmrData as GetEmrData
from utils.GetEmrData import EmrFileAccessDetails
from setuptools_scm import get_version

#from memory_profiler import profile

# set the version using setuptools_scm
# allow for setting the version when redi is imported
try:
    __version__ = get_version()
except:
    __version__ = get_version(root='..', relative_to=__file__)

# Command line default argument values
_person_form_events_service = None
translational_table_tree = None

DEFAULT_DATA_DIRECTORY = os.getcwd()


def main():
    """
    Data processing steps:

    - parse raw XML to ElementTree: "data"
    - call read-in function to load xml into ElementTree

    - parse formEvents.xml to ElementTree
    - call read-in function to load xml into ElementTree

    - parse translationTable.xml to ElementTree
    - call read-in function to load xml into ElementTree

    - add element to data ElementTree for timestamp, redcap form name,
        eventName, formDateField, and formCompletedFieldName
    - write out ElementTree as an XML file
    - call read-in function to load xml into ElementTree

    - update timestamp using collection_date and collection_time
    - write redcapForm name to data ElementTree by a lookup of component ID in translationTable.xml

    - sort data by: study_id, form name, then timestamp, ascending order
    - write formDateField to data ElementTree via lookup of formName in formEvents.xml

    - write formCompletedFieldName to data ElementTree via lookup of formName in formEvents.xml
    - write eventName to data ElementTree via lookup of formName in formEvents.xml

    Example:
    <formName value="chemistry">
        <event name="1_arm_1" />
    </formName>

    - write the Final ElementTree to EAV
    """

    # TODO: UPDATE COMMENT HERE
    global _person_form_events_service

    # obtaining command line arguments for path to configuration directory
    args = docopt(__doc__, help=True)


    #def get_args():
    #    return args

    # capture any cli args passed in that are needed to pass into other funcs.
    data_directory = args['--datadir']
    # we need to access this in nested functions.
    # make it global. CPB made me do it.
    global keep_all_results
    keep_all_results = args['--keep-all']

    if data_directory is None:
        data_directory = DEFAULT_DATA_DIRECTORY

    configuration_directory = args['--config-path']
    if configuration_directory is None:
        configuration_directory = os.path.join(data_directory, "config")


    do_keep_gen_files = args['--keep']
    get_emr_data = args['--emrdata']
    dry_run = args['--dryrun']

    # setup the logger right away
    # configure logger
    #TODO: make logger parameters configurable
    logger = configure_logging(data_directory, args['--verbose'], when='D', interval=1, backup_count=31)

# ______________________________________________________________________________
# commandline switch: -f, --file
# ______________________________________________________________________________
# -f, --file are commandline switches to allow the passing in of a data file to
# RED-I. The file should exist, and it shoudl be a CSV, and it should be
# readable. If no input is specified then use the defaults and look for a file
# called raw.txt in the specified `config` directory.
# ______________________________________________________________________________

    # parse the commandline argument, args requires using long opt if it exists
    # i.e. -f won't work here if --file is also part of the option.
    input_file_path = args['--file']

    # TODO: need to add this to the debug/verbose scaffolding
    # print input_file_path
    # sys.exit(0)

    # check to see if a file was passed in
    if (input_file_path != None):
        # say something nice to the people.
        logger.info("Using file passed in via -f switch. File name: " + input_file_path)
        # check to make sure its a file
        if os.path.isfile(input_file_path):
            #check to see if you can read it
            if os.access(input_file_path, os.R_OK):
                #ok , all is well make the assignment ;)
                raw_txt_file = input_file_path
            else:
                logger.info("File passed in at the commandline cannot be accessed, file: " + input_file_path)
        else:
            logger.info("File passed in at the commandline is not a file: " + input_file_path)

    else:
        raw_txt_file = os.path.join(configuration_directory, 'raw.txt')

    # display version number and quit
    if args['--version']:
        print(__version__)
        print("redi - REDCap Electronic Data Importer")
        print("http://redi.readthedocs.org")
        sys.exit()


    if input_file_path and get_emr_data:
        logger.error("You cannot use -e and -f together.")
        logger.error("RED-I will now terminate.")
        sys.exit()

    # Parsing the config file using a method from module SimpleConfigParser
    settings = SimpleConfigParser.SimpleConfigParser()
    config_file = os.path.join(configuration_directory, 'settings.ini')
    settings.read(config_file)
    # this method reduces the syntax
    settings.set_attributes()

    # creating temporary folder for storing files which may or may not
    # be retained (depending on the value of do_keep_gen_files)
    # When dry run state is on, the files are retained by default
    if dry_run and not do_keep_gen_files:
        do_keep_gen_files = True

    db_path = get_db_path(settings.batch_info_database, data_directory)

    output_files = os.path.join(data_directory, "data")
    _makedirs(output_files)

    # Check if files mentioned in the configuration file exist
    file_list = [
        settings.translation_table_file,
        settings.form_events_file,
        settings.research_id_to_redcap_id,
        settings.component_to_loinc_code_xml
    ]
    read_config(config_file, configuration_directory, file_list)

    _person_form_events_service = PersonFormEventsRepository(\
        os.path.join(output_files, 'person_form_event_tree_with_data.xml'),\
         logger)

    redcap_client = connect_to_redcap(get_email_settings(settings),
                                      get_redcap_settings(settings), dry_run)

    report_file_path = os.path.join(output_files,
                                    settings.report_file_path)

    report_creator = report.ReportCreator(report_file_path, settings.project,
                                          settings.redcap_uri,
                                          settings.is_sort_by_lab_id,
                                          write_element_tree_to_file)

    if settings.send_email:
        report_courier = report.ReportEmailSender(get_email_settings(settings), logger)
    else:
        report_courier = report.ReportFileWriter(os.path.join(output_files,
            settings.report_file_path2), logger)

    # This is the run that loads the data
    _run(config_file, configuration_directory, do_keep_gen_files, dry_run,
         get_emr_data, settings, output_files, db_path, raw_txt_file, redcap_client,
         report_courier, report_creator, args['--resume'],
         args['--skip-blanks'], args['--bulk-send-blanks'], keep_all_results, input_file_path)

    # TODO: post processing will go here


def get_db_path(batch_info_database, database_path):
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    db_path = os.path.join(database_path, batch_info_database)
    return db_path


def _makedirs(data_folder):
    # Like os.makedirs() but suppresses error if path already exists.
    try:
        os.makedirs(data_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e


def _delete_last_runs_data(data_folder):
    _person_form_events_service.delete()
    _remove(os.path.join(data_folder, 'alert_summary.obj'))
    _remove(os.path.join(data_folder, 'rule_errors.obj'))
    _remove(os.path.join(data_folder, 'collection_date_summary_dict.obj'))
    _remove(os.path.join(data_folder, 'sent_events.idx'))


def _remove(path):
    # Like os.remove() but suppresses error if path does not exist
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e


def _fetch_run_data(data_folder):
    person_form_event_tree_with_data = _person_form_events_service.fetch()
    alert_summary = _load(os.path.join(data_folder, 'alert_summary.obj'))
    rule_errors = _load(os.path.join(data_folder, 'rule_errors.obj'))
    collection_date_summary_dict = _load(
        os.path.join(data_folder, 'collection_date_summary_dict.obj'))
    sent_events = SentEvents(os.path.join(data_folder, 'sent_events.idx'))
    bad_ids = _load(os.path.join(data_folder, 'bad_ids.obj'))
    return (alert_summary, person_form_event_tree_with_data, rule_errors, collection_date_summary_dict, sent_events, bad_ids)


def _load(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def _store_run_data(data_folder, alert_summary,
                    person_form_event_tree_with_data, rule_errors,
                    collection_date_summary_dict,
                    bad_ids):
    _person_form_events_service.store(person_form_event_tree_with_data)
    _save(alert_summary, os.path.join(data_folder, 'alert_summary.obj'))
    _save(rule_errors, os.path.join(data_folder, 'rule_errors.obj'))
    _save(collection_date_summary_dict,
          os.path.join(data_folder, 'collection_date_summary_dict.obj'))
    _save(bad_ids, os.path.join(data_folder, 'bad_ids.obj'))


def _save(obj, path):
    with open(path, 'wb') as fp:
        pickle.dump(obj, fp)


def connect_to_redcap(email_settings, redcap_settings, dry_run=False):
    try:
        return RedcapClient(redcap_settings['redcap_uri'],
                            redcap_settings['token'],
                            redcap_settings['verify_ssl'])
    except RequestException as error:
        logger.exception(error)

        if not dry_run:
            logger.info("Sending email to redcap support")
            redi_email.send_email_redcap_connection_error(email_settings)
        sys.exit()


def _run(config_file, configuration_directory, do_keep_gen_files, dry_run,
         get_emr_data, settings, data_folder, database_path, raw_txt_file, redcap_client,
         report_courier, report_creator, resume=False, skip_blanks=False,
         bulk_send_blanks=False, keep_all_results=False, input_file_path=None):
    global translational_table_tree

    assert _person_form_events_service is not None

    # Getting EMR data
    if get_emr_data:
        connection_details = EmrFileAccessDetails(
            settings.emr_sftp_project_name,
            settings.emr_data_file,
            settings.emr_sftp_server_hostname,
            settings.emr_sftp_server_username,
            settings.emr_sftp_server_password,
            settings.emr_sftp_server_port,
            settings.emr_sftp_server_private_key,
            settings.emr_sftp_server_private_key_pass,
            )
        GetEmrData.get_emr_data(configuration_directory, connection_details)

    # save raw file into expected location, config directory + "raw.txt"
    # this is so the prefilters know where to find it
    if keep_all_results:
        with open(raw_txt_file, 'r') as f:
            lines = f.readlines()
            with open(os.path.join(configuration_directory, "raw.txt"), "w") as f2:
                f2.writelines(lines)
        # now that we've written to raw.txt, change raw_txt_file to point to it
        raw_txt_file = os.path.join(configuration_directory, 'raw.txt')

    # load custom pre-processing filters
    pre_filters = load_preproc(settings.preprocessors, configuration_directory)
    # load custom post-processing rules
    rules = load_rules(settings.rules, configuration_directory)

    errors = run_preproc(pre_filters, settings)
    map(logger.warning, errors)

    escaped_file = os.path.join(configuration_directory, 'rawEscaped.txt')
    raw_xml_file = os.path.join(configuration_directory, 'raw.xml')

    # TODO: make this able to run against a local file if desired
    # replace certain characters with escape sequences
    if get_emr_data:
        GetEmrData.data_preprocessing(raw_txt_file, escaped_file)
    if get_emr_data:
        # run csv2xml.py to generate data in xml format
        GetEmrData.generate_xml(escaped_file, raw_xml_file)
    if get_emr_data:
        # delete rawEscaped.txt
        GetEmrData.cleanup(escaped_file)

    # TODO: clean this up as well was the get_emr_ stuff above

    # if either -K or -f are specifed run the steps to make raw.xml
    if (keep_all_results != False or input_file_path != None):
        GetEmrData.data_preprocessing(raw_txt_file, escaped_file)
        GetEmrData.generate_xml(escaped_file, raw_xml_file)
        GetEmrData.cleanup(escaped_file)



    raw_xml_file = os.path.join(configuration_directory, settings.raw_xml_file)
    email_settings = get_email_settings(settings)
    db_path = database_path
    # Insert/load batch row so we can set the `completed` status
    start_time = batch.get_db_friendly_date_time()
    current_batch = _check_input_file(db_path, email_settings, raw_xml_file,
                                  settings,start_time)

    form_events_file = os.path.join(configuration_directory,\
     settings.form_events_file)

    translation_table_file = os.path.join(configuration_directory, \
        settings.translation_table_file)

    if not resume:
        _delete_last_runs_data(data_folder)

        # TODO: Add preproc errors to report

        alert_summary, person_form_event_tree_with_data, rule_errors, \
        collection_date_summary_dict, bad_ids =\
        _create_person_form_event_tree_with_data(
            config_file, configuration_directory, redcap_client,
            form_events_file, raw_xml_file, rules, settings, data_folder,
            translation_table_file, keep_all_results)

        _store_run_data(data_folder, alert_summary,
                        person_form_event_tree_with_data, rule_errors,
                        collection_date_summary_dict, bad_ids)

    (alert_summary, person_form_event_tree_with_data, rule_errors,
     collection_date_summary_dict, sent_events, bad_ids) = _fetch_run_data(data_folder)

    # Data will be sent to REDCap server and email will be sent only if
    # redi.py is not executing in dry run state.
    if not dry_run:
        all_form_events = person_form_event_tree_with_data.xpath("//event")

        # Reduce the specified rate by 5% to account for the overhead
        rate_limit_safe = max(1, \
                math.floor(0.90*int(settings.rate_limiter_value_in_redcap)))
        logger.info("Throttling requests at the rate of {} per minute" \
                .format(rate_limit_safe))

        # Use the new method to communicate with REDCap
        report_data = upload.generate_output(
            person_form_event_tree_with_data, redcap_client,
            rate_limit_safe, sent_events,
            int(settings.max_retry_count), skip_blanks, bulk_send_blanks)

        # Save the time it took to send data to REDCap
        done_time = batch.get_db_friendly_date_time()
        # Update the batch row
        batch.update_batch_entry(database_path,
                                    current_batch['rbID'],
                                    batch.BATCH_STATUS_COMPLETED,
                                    start_time,
                                    done_time)
        duration_dict = {
            'all' : {
                'start': start_time,
                'end': done_time,
            },
        }

        # write person_form_event_tree to file
        write_element_tree_to_file(person_form_event_tree_with_data,\
         os.path.join(data_folder, 'person_form_event_tree_with_data.xml'))
        if len(all_form_events) != len(sent_events):
            logger.warning(
                'Some of the events were not sent to the REDCap server. Please '
                "check the log file or {0}/sent_events.idx".format(data_folder))
        # Add any errors from running the rules to the report
        map(logger.warning, rule_errors)

        if settings.include_rule_errors_in_report:
            report_data['errors'].extend(rule_errors)

        # Add bad research ids to the report
        for bad_id in bad_ids.iteritems():
            bad_id_msg = "Research ID {} present in source data but not in "\
            "target REDCap".format(bad_id[0])
            report_data['errors'].append(bad_id_msg)

        # create summary report
        html_str = report_creator.create_report(
            report_data,
            alert_summary,
            collection_date_summary_dict,
            duration_dict)

        report_courier.deliver(html_str)

    if dry_run:
        logger.info("End of dry run. All output files are ready for review"\
        " in " + data_folder)

    if not do_keep_gen_files:
        shutil.rmtree(data_folder)


def _create_person_form_event_tree_with_data(
        config_file, configuration_directory, redcap_client, form_events_file,
        raw_xml_file, rules, settings, data_folder, translation_table_file, keep_all_results):

    global translational_table_tree
    # parse the raw.xml file and fill the etree rawElementTree
    data = parse_raw_xml(raw_xml_file)

    # check if raw element tree is empty
    if not data:
        # raise an exception if empty
        raise Exception('data is empty')

    # add blank elements to each subject in data tree
    add_elements_to_tree(data)
    # replace fields in raw_xml
    if settings.replace_fields_in_raw_data_xml:
        replace_fields_in_raw_data_xml = os.path.join(\
            configuration_directory, settings.replace_fields_in_raw_data_xml)
        data = replace_fields_in_raw_xml(data, replace_fields_in_raw_data_xml)
    else:
        logger.warning("Parameter 'replace_fields_in_raw_data_xml' missing"\
        " in {0}. Fields will not be replaced".format(config_file))

    data, collection_date_summary_dict = \
    verify_and_correct_collection_date(data, settings.input_date_format)
    # write_element_tree_to_file(data, proj_root+'raw_with_proper_dates.xml')

    # Convert COMPONENT_ID to loinc_code in the raw data
    component_to_loinc_code_xml = os.path.join(configuration_directory, \
                                  settings.component_to_loinc_code_xml)
    component_to_loinc_code_xsd = pkg_resources.resource_filename(
        'redi', 'utils/component_id_to_loinc_code.xsd')
    component_to_loinc_code_xml_tree = validate_xml_file_and_extract_data \
        (component_to_loinc_code_xml, component_to_loinc_code_xsd)
    convert_component_id_to_loinc_code(data, component_to_loinc_code_xml_tree)
    # parse the formEvents.xml file and fill the etree 'form_events_file'
    form_events_tree = parse_form_events(form_events_file)
    forms = form_events_tree.findall("form/name")
    form_Completed_Field_Names = form_events_tree. \
        findall("form/formCompletedFieldName")
    form_data = {}
    for i in range(len(forms)):
        form_data[forms[i].text] = form_Completed_Field_Names[i].text

    # check if form element tree is empty
    if not form_events_tree:
        # raise an exception if empty
        raise Exception('form_events_tree is empty')
    write_element_tree_to_file(form_events_tree, os.path.join(data_folder,\
     'formData.xml'))
    # Create empty events for one subject and save it to the
    # all_form_events.xml
    all_form_events_per_subject = create_empty_events_for_one_subject_helper \
        (form_events_file, translation_table_file)
    write_element_tree_to_file(all_form_events_per_subject,\
     os.path.join(data_folder, 'all_form_events.xml'))
    # parse the translationTable.xml file and fill the
    # etree 'translation_table_file'
    translational_table_tree = parse_translation_table(translation_table_file)
    # check if translational table element tree is empty
    if not translational_table_tree:
        # raise an exception if empty
        raise Exception('translational_table_tree is empty')
    write_element_tree_to_file(translational_table_tree,\
     os.path.join(data_folder, 'translationalData.xml'))
    # update the timestamp for the global element tree
    update_time_stamp(data, settings.input_date_format, settings.output_date_format)
    # write back the changed global Element Tree
    write_element_tree_to_file(data, os.path.join(data_folder,\
     'rawData.xml'))
    # update the redcap form name
    update_redcap_form(data, translational_table_tree, 'undefined')
    # write the element tree
    write_element_tree_to_file(data, os.path.join(data_folder,\
     'rawDataWithFormName.xml'))
    # set all formImportedFieldName value to the value mapped from
    # formEvents.xml
    update_form_imported_field(data, form_events_tree, 'undefined')
    # output raw file to check it
    write_element_tree_to_file(
        data,
        os.path.join(data_folder, 'rawDataWithFormImported.xml'))
    # update the redcapStatusFieldName
    update_recap_form_status(data, translational_table_tree, 'undefined')
    # output raw file to check it
    write_element_tree_to_file(data, os.path.join(data_folder,\
     'rawDataWithFormStatus.xml'))
    # update formDateField
    update_formdatefield(data, form_events_tree)
    # write back the changed global Element Tree
    write_element_tree_to_file(data, os.path.join(data_folder,\
     'rawData.xml'))
    # update formCompletedFieldName
    update_formcompletedfieldname(data, form_events_tree, 'undefined')
    # write back the changed global Element Tree
    write_element_tree_to_file(
        data,
        os.path.join(data_folder, 'rawDataWithFormCompletedField.xml'))
    # update element that holds the name of the redcap field that will hold
    # the datum or value.
    # Also update the name of the redcap field that will hold the units
    update_redcap_field_name_value_and_units(data, translational_table_tree,
                                             'undefined')
    # write back the changed global Element Tree
    write_element_tree_to_file(
        data,
        os.path.join(data_folder, 'rawDataWithDatumAndUnitsFieldNames.xml'))
    # sort the data tree and compress
    sort_element_tree(data, data_folder, keep_all_results)
    write_element_tree_to_file(data, os.path.join(data_folder, \
        'rawDataSortedAfterCompression.xml'))
    # update eventName element
    alert_summary = update_event_name(data, form_events_tree, 'undefined')
    # write back the changed global Element Tree
    write_element_tree_to_file(data, os.path.join(data_folder, \
        'rawDataWithAllUpdates.xml'))

    # Research ID - to - Redcap ID converter
    bad_ids = research_id_to_redcap_id_converter(
        data,
        redcap_client,
        settings.research_id_to_redcap_id,
        configuration_directory)

    person_form_event_tree = create_empty_event_tree_for_study(
        data,
        all_form_events_per_subject)
    # write person_form_event_tree to file
    write_element_tree_to_file(person_form_event_tree,
                               os.path.join(data_folder,\
                                'person_form_event_tree.xml'))
    # copy data to person form event tree
    person_form_event_tree_with_data = copy_data_to_person_form_event_tree \
        (data, person_form_event_tree, form_events_tree)
    # update status field in person form event tree
    updateStatusFieldValueInPersonFormEventTree \
        (person_form_event_tree_with_data, translational_table_tree)
    # write person form event tree with data (both regular fields\
    # and status fields) to file
    write_element_tree_to_file(
        person_form_event_tree_with_data,
        os.path.join(data_folder, 'person_form_event_tree_with_data.xml'))
    # run custom post-processing rules
    person_form_event_tree_with_data, rule_errors = run_rules(
        rules, person_form_event_tree_with_data)
    return alert_summary, person_form_event_tree_with_data, rule_errors, \
    collection_date_summary_dict, bad_ids


def _check_input_file(db_path, email_settings, raw_xml_file, settings,start_time):
    return batch.check_input_file(settings.batch_warning_days, db_path,
                                  email_settings, raw_xml_file,
                                  settings.project,start_time)



def read_config(config_file, configuration_directory, file_list):
    """
    Check if files mentioned in configuration files exist
    """
    for item in file_list:
        if not os.path.exists(os.path.join(configuration_directory, item)):
            logger.error("Required file '{0}' specified in {1} does not "\
                "exist in {2}. Please refer config-example/{3} for sample "\
                "contents of this file. Program will now terminate..."\
                .format(item, config_file, configuration_directory, item))
            sys.exit()

def parse_raw_xml(raw_xml_file):
    """
    Generate an ElementTree from a raw XML file.

    :param raw_xml_file: the input file.
    :return: parsed XML data
    """
    if not os.path.exists(raw_xml_file):
        raise Exception\
            ("Error: raw xml file not found at file not found at "
             + raw_xml_file)
    else:
        raw = open(raw_xml_file, 'r')
        logger.debug("Raw XML file contains {} lines." \
                .format(str(sum(1 for line in raw))))

    parser = etree.XMLParser(remove_comments = True)
    data = etree.parse(raw_xml_file, parser = parser)
    event_sum = len(data.findall(".//subject"))
    logger.debug(str(event_sum) + " total subject entries read into tree.")
    raw.close()
    logger.debug("Raw XML file closed.")
    return data


def parse_form_events(form_events_file):
    """
    Parse the form_events file into an ElementTree

    :param form_events_file: the name of the input file (from the json configuration)
    :return: ElementTree
    """
    if not os.path.exists(form_events_file):
        raise Exception("Error: form events file not found at "
                           + form_events_file)
    else:
        raw = open(form_events_file, 'r')
        logger.info("Form events file contains {} lines." \
                .format(str(sum(1 for line in raw))))

    validate_xml_file_and_extract_data(form_events_file, pkg_resources.resource_filename(
        'redi', 'utils/formEvents.xsd'))
    data = etree.parse(form_events_file)
    event_sum = len(data.findall(".//event"))
    logger.debug(str(event_sum) + " total events read into tree.")
    raw.close()
    logger.debug("Form events file closed.")
    return data


def parse_translation_table(translation_table_file):
    """
    Parse the translationTable.xml into an ElementTree

    :param translation_table_file: the name of the input file
    :return: ElementTree
    """
    if not os.path.exists(translation_table_file):
        raise Exception("Error: translation table file not found at "
                           + translation_table_file)
    else:
        raw = open(translation_table_file, 'r')
        logger.info("Translation table file contains {} lines" \
                .format(str(sum(1 for line in raw))))
    data = etree.parse(translation_table_file)
    event_sum = len(data.findall(".//clinicalComponent"))
    logger.info(str(event_sum) + " total clinicalComponents read into tree.")
    raw.close()
    logger.info("Translation table file closed")
    return data


def add_elements_to_tree(data):
    """
    Add blank elements to fill out in ElementTree.

    Add element to data ElementTree for timestamp, redcap form name, eventName,
    formDateField, and formCompletedFieldName.

    :param data: the input ElementTree from the parsed raw XML file.
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
        element.append(etree.Element("redcapStatusFieldName"))


def update_recap_form_status(data, lookup_data, undefined):
    """Update the redcapStatusFieldName value to all subjects"""
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapStatusFieldName'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapStatusFieldName'

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)


def update_form_imported_field(data, lookup_data, undefined):
    """Update the formImportedFieldName value for all subjects"""
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'formImportedFieldName'
    index_element_in_data = 'redcapFormName'
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    value_in_lookup_data = 'formImportedFieldName'

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)


def write_element_tree_to_file(element_tree, file_name):
    """Write an ElementTree to a file whose name is provided as an argument"""
    logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(
        file_name,
        encoding="us-ascii",
        xml_declaration=True,
        method="xml",
        pretty_print=True)


def update_time_stamp(data, input_date_format, output_date_format):
    """
    Update timestamp using input and output data formats.
    Warnings:
      - we modify the data ElementTree
      - we affect the sorting order of data elements @see #sort_element_tree()
    """
    logger.debug('Updating timestamp to ElementTree')
    for subject in data.iter('subject'):
        # New EMR field SPECIMN_TAKEN_TIME is used in place of Collection Date
        # and Collection Time
        specimn_taken_time = subject.find('DATE_TIME_STAMP').text

        if specimn_taken_time is not None:
            # Converting specimen taken time to redcap accepted time format
            # YYYY-MM-DD

            # construct struct_time structure from String
            # this will accurately pad each part of the time
            # Rule : generic input/output of date format
            temptime = time.strptime(specimn_taken_time, input_date_format)
            # convert struct into a string representation
            date_time = time.strftime(output_date_format, temptime)

            # write the dateTime to ElementTree
            subject.find('timestamp').text = format(date_time)


def update_redcap_form(data, lookup_data, undefined):
    """
    Lookup component ID in translationTable to get the redcapFormName.
    Write the redcapForm name to data
    If component lookup fails, sets formName to undefinedForm
    """
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'redcapFormName'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapFormName'

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)


def sort_element_tree(data, data_folder, keep_all_results):
    """
    Sort element tree based on three given indices.
    @see #update_time_stamp()

    Keyword argument: data
    sorting is based on study_id, form name, then timestamp, ascending order
    """
    # this element holds the subjects that are being sorted
    container = data.getroot()
    container[:] = sorted(container, key=get_key_timestamp, reverse=False)

    #if logger.isEnabledFor(logging.DEBUG):
    logger.debug("sort_element_tree container:")
    #batch.printxml(container)

    # print sorted data before compression for reference
    write_element_tree_to_file(data, os.path.join(data_folder,
        "rawDataSortedBeforeCompression.xml"))

    # TODO: look at adding a switch to RED-I, that will need to be caught here, that
    #       will allow another behavioe here that will let us keep all results vs
    #       the current behavior of sorting the events by timestamp and keeping only
    #       the first one to occur on a given day. Example: whne this feature is
    #       implemented red-i will be able to keep only 1 data point for each day
    #       for 50 days or keep 50 data points that may occur on the same day and
    #       map the 50 into 50 event slots in redcap.
    if (keep_all_results == False):
        compress_data_using_study_form_date(data)

    #batch.printxml(container)

#@profile
def compress_data_using_study_form_date(data):
    """
    This function is removing duplicate results
    which were recorded on same date but different times.
    Warnings:
        - we assume that the passed ElementTree is sorted
        - we skip all "Canceled" results but we want to keep at least one
            so when all results are canceled we keep the first one
        - the passed object is altered

    @see #get_key_date()
    @see #get_key_timestamp()
    @see #sort_element_tree()

    Parameters:
    -----------
    data: the ElementTree object that needs to be `compressed`
    return: none
    """
    data_root = data.getroot()
    buckets = dict()

    # first loop groups the results in buckets
    for subj in data_root.iter('subject'):
        study_id = subj.findtext('STUDY_ID')
        result = subj.findtext('ORD_VALUE')
        clean_result = '' if result is None else result.strip().lower()
        is_canceled = clean_result.startswith('cancel')

        # Because the data is sorted the first element
        # added to the dictionary is the one we keep
        key = get_key_date(subj)

        if key not in buckets:
            buckets[key] = {0: is_canceled}
        else:
            next_index = len(buckets[key])
            update = { next_index: is_canceled }
            buckets[key].update(update)

    #pprint(buckets)

    # second loop removes the 'CanceL(L)eD' results
    for subj in data_root.iter('subject'):
        result = subj.findtext('ORD_VALUE')
        clean_result = '' if result is None else result.strip().lower()
        is_canceled = clean_result.startswith('cancel')

        key = get_key_date(subj)
        key_debug = get_key_timestamp(subj)

        results_count = len(buckets[key])
        canceled_results_count = 0

        for bucket_data in buckets[key]:
            if buckets[key][bucket_data]:
                canceled_results_count += 1

        is_all_canceled = (results_count == canceled_results_count)
        # xpath "//subject[STUDY_ID[text() = '999'] and redcapFormName[text() = 'cbc'] and ...]/@id"

        if results_count > 1 and is_canceled and not is_all_canceled:
            # when there is more than one value in the `bucket`
            # we can skip invalid values
            #print("Remove duplicate result using key: {}".format(key_debug))
            logger.debug("Remove duplicate result using key: {}".format(key_debug))
            subj.getparent().remove(subj)



    filt = dict()

    # third loop filters out all results in a "bucket" except the first one
    for subj in data_root.iter('subject'):
        study_id = subj.findtext('STUDY_ID')
        result = subj.findtext('ORD_VALUE')
        timestamp = subj.findtext("DATE_TIME_STAMP")

        if not timestamp:
            # we can only compress if there is a valid timestamp
            continue

        # Because the data is sorted the first element
        # added to the dictionary is the one we keep
        key = get_key_date(subj)
        key_debug = get_key_timestamp(subj)

        if key in filt:
            logger.debug("Remove duplicate result using key: {}".format(key_debug))
            #print("Remove duplicate result using key: {}".format(key_debug))
            subj.getparent().remove(subj)
            #continue
        else:
           filt[key] = True

    #pprint(filt)


def get_key_timestamp(ele):
    """
    Helper function for #sort_element_tree()
    @see #compress_data_using_study_form_date()

    Parameters:
    -----------
    elem: lxml.etree._Element object for which we build a key
    returns the corresponding quadruple (study_id, form_name, timestamp)
    """

    #batch.printxml(ele)
    study_id    = ele.findtext("STUDY_ID")
    form_name   = ele.findtext('redcapFormName')
    timestamp   = ele.findtext("DATE_TIME_STAMP")
    return (study_id, form_name, timestamp)


def get_key_date(ele,keep_all_results=False):
    """
    Helper function for #compress_data_using_study_form_date()

    Parameters:
    -----------
    elem: lxml.etree._Element object for which we build a key
    returns the corresponding quadruple (study_id, form_name, loinc_code, date)
    """

    #batch.printxml(ele)
    study_id    = ele.findtext("STUDY_ID")
    form_name   = ele.findtext('redcapFormName')
    loinc_code  = ele.findtext('loinc_code')
    timestamp   = ele.findtext("DATE_TIME_STAMP")
    # extract the date portion "2015-01-01" from "2015-01-01 00:00:00"
    date = timestamp.split(" ")[0]
    return (study_id, form_name, loinc_code, date)


def update_formdatefield(data, form_events_tree):
    """
    Write formDateField to data ElementTree via lookup of
    formName in form_events_tree ElementTree
    """

    logger.debug('updating the formDateField')
    # make a dictionary of the relevant elements from the translationTable
    form_event_root = form_events_tree.getroot()
    if form_event_root is None:
        raise Exception('Form Events tree is empty')

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
            # print form_name
            #print('key not found')
            logger.error('formName is empty. so not updating formDateField')
            continue


def update_formcompletedfieldname(data, lookup_data, undefined):
    """function to update formCompletedFieldName in data ElementTree via
        lookup of formName in formEvents ElementTree

    """
    # make a dictionary of the relevant elements from the form_events
    element_to_set_in_data = 'formCompletedFieldName'
    index_element_in_data = 'redcapFormName'
    element_to_find_in_lookup_data = 'form'
    index_element_in_lookup_data = 'name'
    value_in_lookup_data = 'formCompletedFieldName'

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)


def update_redcap_field_name_value_and_units(data, lookup_data, undefined):
    """function to update redcapFieldNameValue and
        redcapFieldNameUnits in data
        ElementTree via lookup of redcapFieldNameValue and
        redcapFieldNameUnits in
        translation table tree

    """
    # set redcapFieldNameValue
    element_to_set_in_data = 'redcapFieldNameValue'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapFieldNameValue'

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)

    # set redcapFieldNameUnits
    element_to_set_in_data = 'redcapFieldNameUnits'
    index_element_in_data = 'loinc_code'
    element_to_find_in_lookup_data = 'clinicalComponent'
    index_element_in_lookup_data = 'loinc_code'
    value_in_lookup_data = 'redcapFieldNameUnits'
    undefined = "redcapFieldNameUnitsUndefined"

    update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined)


def update_data_from_lookup(
        data,
        element_to_set_in_data,
        index_element_in_data,
        lookup_data,
        element_to_find_in_lookup_data,
        index_element_in_lookup_data,
        value_in_lookup_data,
        undefined):
    """Update a single field in an element tree based on a lookup in another
        element tree
    :param data: an element tree with a field that needs to be set
    :param element_to_set_in_data: element that will be set
    :param index_element_in_data: element in data that wil be looked up
            in lookup table where value of element to be set wil be found
    :param lookup_data: an element tree that contains, the lookup data
    :param element_to_find_in_lookup_data: parameter for the initial
            findall in the lookup data
    :param index_element_in_lookup_data: the element in the lookup data
            that will be the key in the lookup table
    :param value_in_lookup_data: element in the lookup data that provides
            the value in the lookup table
    :param undefined: a string to be returned for all failed lookups in
            the lookup table
    """

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

    count = 0
    for child in data_root:
        # get the element text, but set a default value of undefined for
        # each look up failure
        key = child.findtext(index_element_in_data)
        new_element_text = lookup_table.get(key, undefined)
        element_to_set = child.find(element_to_set_in_data)
        element_to_set.text = new_element_text


def update_event_name(data, lookup_data, undefined):
    """function to update eventName to data ElementTree via lookup of formName
        in formEvents ElementTree

    """
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
    first_time = True
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
            logger.info("form_name is marked as undefined.")
            element_to_set.text = undefined
        elif timestamp == '':
            # Log this as bad data we are skipping
            logger.debug(
                "update_event_name: timestamp is missing.  Skipping form %s for subject %s",
                form_name,
                study_id)
        else:
            lookup_table_length = len(lookup_table[form_name])
            current_record_group = string.join([study_id, form_name], "_")
            current_timestamp_group = \
                string.join([study_id, form_name, timestamp], "_")
        # if keep_all_results:
        #     logger.info("event_index: {}".format(str(event_index)))

            if last_record_group != current_record_group:
                # Check that the event counter form the previous loop did not
                # exceed the size of the event list.  If it did we should
                # issue a warning

                if old_form_name is not "dummy" and \
                event_index > len(lookup_table[old_form_name]):
                    max_event_alert.append("Exceeded event list for record "\
                        "group with Subject ID.: " + last_study_id + " and "\
                        "Form Name: " + last_form_name + ". Event count "\
                        "of " + str(event_index) + " exceeds maximum of " + \
                        str(len(lookup_table[old_form_name])))
                    logger.warn('update_event_name: %s', max_event_alert)

                # reset the event counter so we can restart from the top
                # of the list. We have moved to a new group
                logger.debug("update_event_name: Move to new record group: %s",
                             current_record_group)
                logger.debug("update_event_name: Move to new record group: \
                        changing last_timestamp_group %s",
                             current_timestamp_group)

                last_record_group = current_record_group
                last_study_id = study_id
                last_form_name = form_name
                last_timestamp_group = current_timestamp_group
                event_index = 0
                # reset first_time if we're keeping all results
                # so we don't increment event_index on the first time through
                if keep_all_results:
                    first_time = True

            if last_timestamp_group != current_timestamp_group:
                # move to the next event
                logger.debug("update_event_name: Move to next event: " +
                             current_timestamp_group)
                #if not first_time:
                event_index += 1
                last_timestamp_group = current_timestamp_group
            else:
                # this handles the condition where there are two medications on the same day that look identical
                # the timestamp group doesn't change in that case, so we much increment it here.
                if (last_timestamp_group == current_timestamp_group) and keep_all_results:
                    if first_time:
                        #logger.info("where event_index: {}".format(event_index))
                        first_time = False
                    elif not first_time:
                        event_index +=1

            # note which form we were on
            old_form_name = form_name
            # check that we have not exceeded the event count for this form.
            # If we have we must issue a warning
            if event_index < lookup_table_length:
                logger.debug("update_event_name: eventName: %s event_index: %s\
                redcapFieldName: %s current_timestamp_group: %s",
                             str(lookup_table[form_name][event_index]),
                             str(event_index),
                             redcap_field_name_value,
                             str(current_timestamp_group))
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
                field_key = connector_string.join(
                    [study_id, form_name, redcap_field_name_value, timestamp, collection_time])
                # print field_key
                distinct_value[field_key] += 1
                if distinct_value[field_key] > 1:
                    logger.debug("update_event_name: multiple values \
                        found for field %s", field_key)
            else:
                element_to_set.text = undefined
                logger.debug("update_event_name: lookup_table_length exceeded.\
                  event_index: %s", str(event_index))
    return {
        'max_event_alert': max_event_alert,
        'multiple_values_alert': multiple_values_alert}


# @TODO: remove settings from signature
def research_id_to_redcap_id_converter(
        data, redcap_client, research_id_to_redcap_id, configuration_directory):
    """
    This function converts the research_id to redcap_id
     1. prepare a dictionary with [key, value] --> [study_id, redcap_id]
     2. replace the element tree study_id with the new redcap_id's
     for each bad id, log it as warn.

    Example of xml fragment produced:
<subject lab_id="999-0001">
    <NAME>HEMOGLOBIN</NAME>
    <loinc_code>1534435</loinc_code>
    <RESULT>1234</RESULT>
...
    <STUDY_ID>1</STUDY_ID> <!-- originally this was "999-0001" -->
</subject>

    Note: The next function which reads the "data" tree
        is #create_empty_event_tree_for_study()
    """
    # read each of the study_id's from the data etree
    study_id_recap_id_dict = {}

    # Configuration data from the mapping xml
    mapping_xml = os.path.join(configuration_directory,
     research_id_to_redcap_id)

    # read the field names from the research_id_to_redcap_id_map.xml
    # check for file existance
    if not os.path.exists(mapping_xml):
        raise Exception(
            "Error: research id to redcap id fieldname xml not found at " +
            mapping_xml)

    mapping_data = etree.parse(mapping_xml)
    root = mapping_data.getroot()
    redcap_id_field_name = root.findtext('redcap_id_field_name')
    research_id_field_name = root.findtext('research_id_field_name')

    if research_id_field_name is None or research_id_field_name == '':
        logger.error(
            'research_id_field_name tag in file %s is not present', mapping_xml)
        raise Exception(
            'research_id_field_name tag in file %s is not present', mapping_xml)

    if redcap_id_field_name is None or redcap_id_field_name == '':
        logger.error(
            'redcap_id_field_name tag in file %s is not present', mapping_xml)
        raise Exception(
            'redcap_id_field_name tag in file %s is not present', mapping_xml)

    # query the redcap for the response with redcap id's
    response = redcap_client.get_data_from_redcap(
        fields_to_fetch=[
            research_id_field_name,
            redcap_id_field_name])
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

        # if the study id is not null populate the dictionary
        if study_id is not None and study_id != '' and study_id in redcap_dict:
            # if the study_id is in the dictionary then replace it by the redcap_id
            lab_id_ele = subject.find('STUDY_ID')

            # save the original subject id from the lab data as an attribute
            subject.set('lab_id', lab_id_ele.text)
            lab_id_ele.text = redcap_dict[study_id]
        elif study_id is not None and study_id != '' and study_id not in redcap_dict:
            # add the bad research id to list of bad ids
            bad_ids[study_id] += 1
            data.getroot().remove(subject)
        else:
            logger.error(
                'Error: research id to redcap id: study_id is invalid')

    for bad_id in bad_ids.iteritems():
        logger.warn('Bad research id %s found %s times', bad_id[0], bad_id[1])

    return bad_ids


def configure_logging(data_folder, verbose=False, when='D', interval=1, backup_count=31):
    """Configures the Logger"""

    # create logger for our application
    application_name = 'redi'
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    global logger
    logger = logging.getLogger(application_name)

    #Set log level for requests module
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    # create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    root_logger.addHandler(console_handler)

    # make sure we can write to the log
    log_folder = os.path.join(data_folder, "log")
    _makedirs(log_folder)
    suffix = '_' + str(date.today())
    filename = os.path.join(log_folder, application_name + suffix + '.log')

    # create a file handler
    file_handler = None
    try:
        file_handler = TimedRotatingFileHandler(filename, when, interval, backup_count)
    except IOError:
        logger.exception('Could not open file for logging "%s"', filename)
        raise

    if file_handler:
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        #logger.info('Logging to the file: "%s"' % filename)
        root_logger.addHandler(file_handler)
    else:
        logger.warning('File logging has been disabled.')

    return logger


def create_empty_events_for_one_subject_helper(
        form_events_file,
        translation_table_file):
    """
    This function creates new copies of the form_events_tree and translation_table_tree and calls create_empty_events_for_one_subject
    :param form_events_file: This parameter holds the path of form_events file
    :param translation_table_file: This parameter holds the path of translation_table file
    """
    form_events_tree = parse_form_events(form_events_file)
    translation_table_tree = parse_translation_table(translation_table_file)
    return create_empty_events_for_one_subject(
        form_events_tree,
        translation_table_tree)


def create_empty_events_for_one_subject(
        form_events_tree,
        translation_table_tree):
    #logger.debug('Creating all form events template for one subject')

    root = etree.Element("all_form_events")
    form_event_root = form_events_tree.getroot()
    translation_table_root = translation_table_tree.getroot()
    if translation_table_root is None:
        raise Exception('translation table tree is empty')
    if form_event_root is None:
        raise Exception('Form Events tree is empty')

    translation_table_dict = {}

    for component in translation_table_root.iter('clinicalComponent'):
        translation_table_dict[component.find('redcapFormName').text] = set()

    for component in translation_table_root.iter('clinicalComponent'):
        form_name = component.find('redcapFormName').text
        if component.find('redcapFieldNameValue') is not None:
            translation_table_dict[form_name].add(
                component.find('redcapFieldNameValue').text)
        if component.find('redcapFieldNameUnits') is not None:
            translation_table_dict[form_name].add(
                component.find('redcapFieldNameUnits').text)
        if component.find('redcapStatusFieldName') is not None:
            translation_table_dict[form_name].add(
                component.find('redcapStatusFieldName').text)

    for form in form_event_root.iter('form'):
        for child in form:
            form_child = child.tag
            if form_child.startswith("form"):
                try:
                    if form_child != 'formCompletedFieldValue' and form_child != 'formImportedFieldValue':
                        translation_table_dict[
                            form.find('name').text].add(
                            child.text)
                except KeyError as e:
                    translation_table_dict[form.find('name').text] = set()
                    translation_table_dict[
                        form.find('name').text].add(
                        child.text)
                form.remove(child)
        all_fields = etree.Element("allfields")
        try:
            for field in translation_table_dict[form.find('name').text]:
                field_tag = etree.SubElement(all_fields, "field")
                name = etree.SubElement(field_tag, "name")
                name.text = field
                value = etree.SubElement(field_tag, "value")
        except KeyError as e:
            logger.exception('There are no fields in this form.')
            raise

        for child in form.iter('event'):
            status_element = etree.Element("status")
            status_element.text = 'unsent'
            child.append(status_element)
            child.insert(
                child.index(
                    child.find('status')) + 1,
                etree.XML(
                    etree.tostring(
                        all_fields,
                        method='html',
                        pretty_print=True)))
        etree.strip_tags(form, 'allfields')

        root.append(form)
    tree = etree.ElementTree(root)
    return tree


def create_empty_event_tree_for_study(raw_data_tree, all_form_events_tree):
    """
    This function uses raw_data_tree and all_form_events_tree and creates
    a person_form_event_tree for study

    :param raw_data_tree: This parameter holds raw data tree
    :param all_form_events_tree: This parameter holds all form events tree
    """
    logger.info('Creating all form events template for all subjects')

    pfe_element = etree.Element("person_form_event")
    raw_data_root = raw_data_tree.getroot()
    all_form_events_root = all_form_events_tree.getroot()
    if raw_data_root is None:
        raise Exception('Raw data tree is empty')
    if all_form_events_root is None:
        raise Exception('All form Events tree is empty')

    subjects_dict = {}

    # Collect the `study_id => lab_id` mappings
    for subject in raw_data_root.iter('subject'):
        study_id = subject.findtext('STUDY_ID')
        subjects_dict[study_id] = subject.attrib['lab_id']

    if not subjects_dict:
        raise Exception("There are no subjects in the raw data. " \
                "This can be caused by an incorrect input file or "\
                "by lack of enrollment data in the REDCap database." )

    for subject_id in subjects_dict.iterkeys():
        person = etree.Element("person")
        # Copy `lab_id` attribute from `subject` to `person` element
        person.set('lab_id', subjects_dict.get(subject_id))
        study_id = etree.SubElement(person, "study_id")
        study_id.text = subject_id
        person_index = person.index(person.find('study_id')) + 1

        # insert the pretty-fied form events
        pretty_form_events = etree.XML(
            etree.tostring(all_form_events_root, method='html', pretty_print=True))
        person.insert(person_index, pretty_form_events)
        pfe_element.append(person)

    return etree.ElementTree(pfe_element)

def setStat(
        event,
        translation_table_dict,
        translation_table_status_field_text_list):
    """
    Ruchi Vivek Desai, May 13 2014
    to assist the updateStatusFieldValueInPersonFormEventTree function
    """
    # iterates over all fields under event (passed as parameter) in source file
    for field in event.iter('field'):  # loop3
        value = field.find('value')
        if (value is not None and value.text is not None):
            #logging.info("text is missing")
            continue

        name = field.find('name')
        if (name is None):
            #logging.info("tag is missing")
            continue

        is_status_field = name.text in translation_table_status_field_text_list
        if (is_status_field):
            #logging.info("This tag needs to be skipped as it might stand for status")
            continue

        doesnt_have_status_field = name.text not in translation_table_dict or translation_table_dict[
            name.text][0] == ""
        if (doesnt_have_status_field):
            #logging.info( "This tag needs to be skipped as it might stand for form name")
            continue  # name could have been a redcap form name like cbc_lbdtc

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


def updateStatusFieldValueInPersonFormEventTree(
        person_form_event_tree,
        translational_table_tree):
    """
    Ruchi Vivek Desai, May 13 2014
    This function updates the status field value with either NOT_DONE (value in the translation table)
    or empty string based on certain conditions
    """
    # Get root of peron form event tree
    person_form_event__tree_root = person_form_event_tree.getroot()
    if (person_form_event__tree_root is None):
        # Log error: Person Form Event Tree is empty
        raise Exception('Person Form Event Tree is empty')

    else:
        # Get root of translation table
        translation_table_root = translational_table_tree.getroot()
        if (translation_table_root is None):
            # Log error: Translation Table Tree is empty
            raise Exception("Translation Table Tree is empty")
        else:
            # This list contains text values of redcapStatusFieldName, to avoid
            # searching for elements with this text later in setStat function
            translation_table_status_field_text_list = [
                x.text for x in translation_table_root.iter('redcapStatusFieldName') if x.text is not None]
            # Parse translation table and make a dictionary to store the person
            # form event tree fields along with their respective status field
            # info
            translation_table_dict = {}
            for clinical_component in translation_table_root:
                if (clinical_component is None):
                    continue
                else:
                    redcap_status_field_name = clinical_component.findtext(
                        "redcapStatusFieldName",
                        "")
                    redcap_status_field_value = clinical_component.findtext(
                        "redcapStatusFieldValue",
                        "")

                    # For every redcap_field other than redcapStatusFieldName,
                    # redcapFieldNameUnits, redcapFieldNameUnitsDescriptiveText,
                    # and redcapStatusFieldValue in this clinical_component add
                    # an entry, {redcap_field.text: [redcapStatusFieldName,
                    # redcapStatusFieldValue]} to translation_table_dict
                    for redcap_field in clinical_component:
                        if (redcap_field is None):
                            continue
                        elif (redcap_field.tag == "redcapFormName"
                                or redcap_field.tag == "redcapStatusFieldName"
                                or redcap_field.tag == "redcapStatusFieldValue"
                                or redcap_field.tag == "redcapFieldNameUnits"
                                or redcap_field.tag == "redcapFieldNameUnitsDescriptiveText"):
                            continue
                        elif (redcap_field.text in translation_table_dict):
                            continue
                        else:
                            translation_table_dict[
                                redcap_field.text] = [
                                redcap_status_field_name,
                                redcap_status_field_value]
                    # End of for redcap_field in clinical_component:
            # End of for clinical_component in translation_table_root:
        # At this point we have the dictionary for the translation table ready

        # For every event in person form event tree, get the text of 'value', which is a descendant of event (child of field), and add it to field_values
        # This checks if the event is completely blank or has some values. We
        # need to update the status field only if the event has some values
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
                # End of for value in event.iter('value'):
                if (field_values == ""):
                    continue
                else:
                    setStat(
                        event,
                        translation_table_dict,
                        translation_table_status_field_text_list)

        # Write the modified tree to an xml file as output
        # person_form_event_tree.write("op1.xml")


def copy_data_to_person_form_event_tree(
        raw_data_tree,
        person_form_event_tree,
        form_events_tree):
    """
    This function copies data from the raw_data_tree to the person_form_event_tree

    :param raw_data_tree: This parameter holds raw data tree
    :param person_form_event_tree: This parameter holds person form event tree
    :param form_events_tree: This parameter holds form events tree
    """
    logger.debug('Copying data to person form event tree')
    raw_data_root = raw_data_tree.getroot()
    person_form_event_tree_root = person_form_event_tree.getroot()
    form_event_root = form_events_tree.getroot()
    if raw_data_root is None:
        raise Exception('Raw data tree is empty')
    if person_form_event_tree_root is None:
        raise Exception('Person Form Event tree is empty')
    if form_event_root is None:
        raise Exception('Form Events tree is empty')

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

            if study_id_object is None:
                raise Exception('Missing required field STUDY_ID')
            else:
                subject_id = study_id_object.text

            if formNameObject is None:
                raise Exception('Missing required field redcapFormName')
            else:
                formName = formNameObject.text
                if formName == 'undefined':
                    continue

            if fieldNameObject is None:
                raise Exception(
                    'Missing required field redcapFieldNameValue')
            else:
                redcapFieldName = fieldNameObject.text

            if fieldValueObject is None:
                raise Exception('Missing required field RESULT')
            else:
                redcapFieldValue = fieldValueObject.text

            if dateFieldObject is None:
                raise Exception('Missing required field formDateField')
            else:
                dateField = dateFieldObject.text

            if dateValueObject is None:
                raise Exception('Missing required field timestamp')
            else:
                dateValue = dateValueObject.text

            if fieldUnitsNameObject is None:
                raise Exception(
                    'Missing required field redcapFieldNameUnits')
            else:
                redcapFieldUnitsName = fieldUnitsNameObject.text

            if fieldUnitsValueObject is None:
                raise Exception('Missing required field REFERENCE_UNIT')
            else:
                redcapFieldUnitsValue = fieldUnitsValueObject.text

            form = person_form_event_tree_root.xpath(
                "person/study_id[.='" +
                subject_id +
                "']/../all_form_events/form/name[.='" +
                formName +
                "']")

            if len(form) < 1:
                raise Exception(
                    'Form named ' +
                    formName +
                    ' Not Found in person form event tree for subject ' +
                    subject_id)

            logger.debug(
                'copy_data_to_person_form_event_tree: ({}, {}, {}, {}, {}, {})'.format(
                    subject_id, formName, eventName, dateValue, redcapFieldName, redcapFieldUnitsName))

            # Copy the first three data fields into the PFE Tree
            path = "person/study_id[.='" + subject_id + "']/../all_form_events/form/name[.='" + \
                formName + "']/../event/name[.='" + eventName + "']/../field"
            fields = person_form_event_tree_root.xpath(path)
            fieldValues = ""

            for node in fields:
                if node.find("name").text == redcapFieldName:
                    node.find("value").text = redcapFieldValue
                    fieldValues = fieldValues + \
                        convert_none_type_object_to_empty_string(redcapFieldValue)
                    continue

                if node.find("name").text == dateField:
                    node.find("value").text = dateValue
                    fieldValues = fieldValues + \
                        convert_none_type_object_to_empty_string(dateValue)
                    continue

                if node.find("name").text == redcapFieldUnitsName:
                    node.find("value").text = redcapFieldUnitsValue
                    fieldValues = fieldValues + \
                        convert_none_type_object_to_empty_string(redcapFieldUnitsValue)
                    continue

            # If we had values in any of the first three fields, copy the
            # form_completed and imported fields
            if fieldValues:
                completedFieldValue = person_form_event_tree_root.xpath(
                    "person/study_id[.='" +
                    subject_id +
                    "']/../all_form_events/form/name[.='" +
                    formName +
                    "']/../event/name[.='" +
                    eventName +
                    "']/../field/name[.='" +
                    formCompletedField.text +
                    "']/../value")
                completedFieldValue[0].text = form_event_root.xpath(
                    "form/name[.='" + formName + "']/../formCompletedFieldValue")[0].text

                form_imported_field_name = subject.findtext("formImportedFieldName", default="")
                imported_field_value = person_form_event_tree_root.xpath(
                    "person/study_id[.='{subject_id}']/../"
                    "all_form_events/form/name[.='{form_name}']/../event/"
                    "name[.='{event_name}']/../field/"
                    "name[.='{form_imported_field_name}']/../value".format(
                        subject_id=subject_id,
                        form_name=formName,
                        event_name=eventName,
                        form_imported_field_name=form_imported_field_name))

                if imported_field_value:
                    try:
                        imported_field_value[0].text = form_event_root.xpath(
                            "form/name[.='" + formName + "']/../formImportedFieldValue")[0].text
                        assert imported_field_value[0].text
                    except (IndexError, AssertionError):
                        raise Exception('formImportedField not set properly in the person form event tree')

                if not completedFieldValue[0].text:
                    raise Exception(
                        'formCompletedField not set properly in the person form event tree')

    tree = etree.ElementTree(person_form_event_tree_root)
    return tree


def convert_none_type_object_to_empty_string(my_object):
    """
    replace noneType objects with an empty string. Else return the object.
    """
    return ('' if my_object is None else my_object)


def convert_component_id_to_loinc_code(data, component_to_loinc_code_xml_tree):
    """
    This function converts COMPONENT_ID in raw data to loinc_code based on the mapping provided in the xml file

    :param data: Raw data xml tree
    :param component_to_loinc_code_xml_tree: COMPONENT_ID to loinc_code mapping xml file tree.

    """
    component2loinc_root = component_to_loinc_code_xml_tree.getroot()
    if component2loinc_root is None:
        raise Exception('component_to_loinc_code_xml is empty')

    for component in component2loinc_root.iter('component'):
        source_name = component.findtext('source/name')
        source_value = component.findtext('source/value')
        target_name = component.findtext('target/name')
        target_value = component.findtext('target/value')
        if source_name and source_value and target_name:
            path = "subject/" + source_name + "[.='" + source_value + "']/.."
            subjects_to_change = data.xpath(path)
            if len(subjects_to_change) < 1:
                logger.debug(
                    'There are no matching sujects to modify in the Raw Data')
            for subject in subjects_to_change:
                new_target_element = etree.Element(target_name)
                new_target_element.text = target_value
                source_element = subject.find(source_name)
                subject.replace(source_element, new_target_element)
        else:
            raise Exception(
                "Elements source/name and Source/value are not present in the component_to_loinc_code xml")
    return data


def validate_xml_file_and_extract_data(xmlfilename, xsdfilename):
    """
    This function is responsible for validating xml file against an xsd and to extract data from xml if validation succeeds

    :param xmlfilename: This parameter holds the path to the xml file
    :param xsdfilename: This parameter holds the path to the xsd file
    """
    if not os.path.exists(xsdfilename):
        raise Exception("Error: " + xsdfilename + " xsd file not found at "
                           + xsdfilename)
    else:
        xsdfilehandle = open(xsdfilename, 'r')
        logger.debug(xmlfilename + " Xsd file read in. ")

    xsd_tree = etree.parse(xsdfilename)
    xsd = etree.XMLSchema(xsd_tree)

    if not os.path.exists(xmlfilename):
        raise Exception("Error: " + xmlfilename + " xml file not found at "
                           + xmlfilename)
    else:
        xmlfilehandle = open(xmlfilename, 'r')
        logger.info(" {} file contains {} lines." \
                .format(xmlfilename, str(sum(1 for line in xmlfilehandle))))

    xml = etree.parse(xmlfilename)
    if not xsd.validate(xml):
        raise Exception(
            "XSD Validation Failed for xml file %s and xsd file %s",
            xmlfilename,
            xsdfilename)
    return xml


def replace_fields_in_raw_xml(data, fields_to_replace_xml):
    """
    replace_fields_in_raw_xml:
    This function renames all fields which need renaming.Fields which need renaming are read from the xml file.
    Parameters:
        data: Raw data xml tree
        fields_to_replace_xml: Path to xml file which has list of fields which need renaming.

    """
    file_path = fields_to_replace_xml
    if not os.path.exists(file_path):
        raise Exception(
            "Error: " +
            fields_to_replace_xml +
            " xml file not found at " +
            fields_to_replace_xml)
    else:
        fields_to_replace_xml_handle = open(file_path, 'r')
        logger.info(fields_to_replace_xml + " Xml file read in. ")

    fields_to_replace_xml_tree = etree.parse(file_path)
    fields_to_replace_xml_tree_root = fields_to_replace_xml_tree.getroot()
    if fields_to_replace_xml_tree_root is None:
        raise Exception('replace_fields_in_raw_data.xml is empty')

    for field in fields_to_replace_xml_tree_root.iter('field'):
        source = field.findtext('source')
        target = field.findtext('target')
        for subject in data.iter('subject'):
            source_element = subject.find(source)
            if source_element is not None:
                new_target_element = etree.Element(target)
                new_target_element.text = source_element.text
                subject.replace(source_element, new_target_element)
    return data


def load_rules(rules, root='./'):
    """
    Load custom post-processing rules.

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
    if not rules:
        return {}

    loaded_rules = {}

    for (rule, path) in ast.literal_eval(rules).iteritems():
        module = None
        if os.path.exists(path):
            module = imp.load_source(rule, path)
        elif os.path.exists(os.path.join(root, path)):
            module = imp.load_source(rule, os.path.join(root, path))

        assert module is not None
        assert module.run_rules is not None

        loaded_rules[rule] = module

    logger.info("Loaded %s post-processing rule(s)" % len(loaded_rules))
    return loaded_rules


def load_preproc(preprocessors, root='./'):
    """
    Copied and modified version of load_rules function.
    TODO: fix load_rules and load_prerules for better parallelism

    """
    if not preprocessors:
        return {}

    loaded = {}

    for (preprocessor, path) in ast.literal_eval(preprocessors).iteritems():
        module = None
        if os.path.exists(path):
            module = imp.load_source(preprocessor, path)
        elif os.path.exists(os.path.join(root, path)):
            module = imp.load_source(preprocessor, os.path.join(root, path))

        assert module is not None
        assert module.run_processing is not None

        loaded[preprocessor] = module

    logger.info("Loaded {} pre-processing script{}".format(
        len(loaded), 's' if len(loaded) != 1 else 0))
    return loaded


def run_preproc(preprocessors, settings):
    # TODO figure out if this creates a sub process or not
    # TODO need to check for program exe3cution otherwise give error
    logger.info("Running preprocessing rules")
    errors = []

    # iterate through sorted list of preprocessors
    for preprocessor in sorted(preprocessors):
        # use original dict of preprocessors to get module name
        module = preprocessors[preprocessor]
        try:
            logger.info("Running preprocessing rule: %s %s", preprocessor, module)
            module.run_processing(settings, redi=sys.modules[__name__],
                                  logger=logging)
        except Exception as e:
            message_format = 'Error processing rule "{0}". {1} {2}'
            if not hasattr(e, 'errors'):
                errors.append(message_format.format(preprocessor, e.message, e.args))
                continue
            for error in e.errors:
                errors.append(message_format.format(preprocessor, error, e.args))

    return errors


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


def verify_and_correct_collection_date(data, input_date_format):
    # this dictionary keeps a track of total specimen taken times and the
    # number of times specimen taken date is missing
    collection_date_summary_dict = {'total': 0, 'blank': 0}
    for subject in data.iter('subject'):
        study_id = subject.findtext('STUDY_ID')
        collection_date_summary_dict['total'] += 1
        collection_date_element = subject.find('DATE_TIME_STAMP')
        result_date_element = subject.find('RESULT_DATE')
        # If DATE_TIME_STAMP tag is present but it has no text (ie blank tag)
        # and if RESULT_DATE is present, then subtract 4 from RESULT_DATE and
        # assign that value to DATE_TIME_STAMP
        if collection_date_element is not None and \
        result_date_element is not None:
            if not collection_date_element.text:
                # subtract 4 days from result date and assign the value to
                # date_time_stamp
                result_date_object = datetime.strptime(
                    result_date_element.text, input_date_format) - \
                timedelta(days=4)
                collection_date_element.text = str(result_date_object)
                collection_date_summary_dict['blank'] += 1
            # else do nothing as DATE_TIME_STAMP does have a value

        # else if DATE_TIME_STAMP tag is not present, create a new tag by the
        # name DATE_TIME_STAMP and add this to the data ElementTree and assign
        # to it the value RESULT_DATE - 4
        elif collection_date_element is None and \
        result_date_element is not None:
            new_collection_date_element = etree.Element('DATE_TIME_STAMP')
            # subtract 4 days from result date and assign the value to
            # date_time_stamp
            result_date_object = datetime.strptime(
                result_date_element.text, input_date_format) - \
            timedelta(days=4)
            new_collection_date_element.text = str(result_date_object)
            subject.replace(result_date_element, new_collection_date_element)
            collection_date_summary_dict['blank'] += 1
            continue
        else:
            continue
        subject.remove(result_date_element)
    if collection_date_summary_dict['blank'] > 0:
        logger.debug("There were {0} out of {1} blank specimen taken times "\
            "in this run.".format(collection_date_summary_dict['blank'],
                collection_date_summary_dict['total']))
    return data, collection_date_summary_dict


def get_email_settings(settings):
    """
    Helper function for grouping email-related properties
    """
    email_settings = {}
    email_settings['smtp_host_for_outbound_mail'] = settings.smtp_host_for_outbound_mail
    email_settings['smtp_port_for_outbound_mail'] = settings.smtp_port_for_outbound_mail
    email_settings['redcap_support_sender_email'] = settings.redcap_support_sender_email
    email_settings['redcap_support_receiving_list'] = \
            settings.redcap_support_receiver_email.split() if settings.redcap_support_receiver_email else []
    email_settings['redcap_uri'] = settings.redcap_uri
    email_settings['batch_warning_days'] = settings.batch_warning_days
    email_settings['batch_report_sender_email'] = settings.sender_email
    email_settings['batch_report_receiving_list'] = \
            settings.receiver_email.split() if settings.receiver_email else []
    email_settings['site_name'] = settings.project
    return email_settings

def get_redcap_settings(settings):
    """
    Helper function for grouping redcap connection properties
    """
    redcap_settings = {}
    redcap_settings['redcap_uri'] = settings.redcap_uri
    redcap_settings['token'] = settings.token
    redcap_settings['rate_limiter_value_in_redcap'] = settings.rate_limiter_value_in_redcap
    redcap_settings['verify_ssl'] = settings.verify_ssl
    return redcap_settings


class PersonFormEventsRepository(object):
    """Wrapper for the person-form-events XML file"""
    def __init__(self, filename, logger=None):
        # simple test to catch obvious errors with a filename supplied
        self._filename = filename
        self._logger = logger

    def delete(self):
        try:
            os.remove(self._filename)
        except OSError:
            # It is okay that the file we wanted to delete does not exist
            pass

    def fetch(self):
        return etree.parse(self._filename)

    def store(self, pfe_tree):
        if self._logger:
            self._logger.debug('Writing ElementTree to %s', self._filename)
        pfe_tree.write(self._filename,
                       encoding="us-ascii",
                       xml_declaration=True,
                       method="xml",
                       pretty_print=True)


class SentEvents(object):
    """
    List of form events that have been sent to REDCap

    :param filename: file location
    :param writer: delegate called after an event has been marked sent
    :param reader: function to read previously sent events from disk
    """
    def __init__(self, filename, writer=None, reader=None):
        self.filename = filename
        self._persist = writer or self._append
        loader = reader or self._readall
        self.sent_events = loader(filename)

    def __len__(self):
        return len(self.sent_events)

    def mark_sent(self, study_id_key, form_name, event_name):
        form_event_key = study_id_key, form_name, event_name
        self.sent_events.append(form_event_key)
        self._persist(self.sent_events, self.filename)

    def was_sent(self, study_id_key, form_name, event_name):
        form_event_key = study_id_key, form_name, event_name
        return form_event_key in self.sent_events

    @staticmethod
    def _readall(filename):
        # Reads events as a list of tuples (default reader delegate)
        try:
            with open(filename, 'r') as fp:
                return [ast.literal_eval(line) for line in fp]
        except IOError:
            return []

    @staticmethod
    def _append(values, filename):
        # Appends the last value to the file (default handler of on_marked_sent)
        if not values:
            return

        with open(filename, 'a') as fp:
            fp.write(str(values[-1]))
            fp.write(os.linesep)


if __name__ == "__main__":
    main()
