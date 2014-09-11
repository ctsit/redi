"""
redi_lib.py

    Stores a collection of utility functions used by redi.py
"""

__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 2-Clause"

import datetime
import os
import stat
import time
import ast
from redcap import RedcapError
import tempfile
import sqlite3 as lite
import md5
import hashlib
import redi
import utils.redi_email as redi_email
from utils.redcapClient import redcapClient
from requests import RequestException
from lxml import etree
import logging
import sys
import collections
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_DATA_DIRECTORY = os.getcwd()


def get_child_text_safely(etree, ele):
    """
    Convenience function
    @see _send_person_form_data_to_redcap()
    """

    ele = etree.find(ele)
    if ele.text is None:
        return ''
    else:
        return ele.text


def handle_errors_in_redcap_xml_response(redcap_response, form_summary):
    """
    This function checks for any errors in the redcap response and
        update report data if there are any errors.
    Parameters:
        :redcap_response: holds the response from REDCap
        :form_summary: holds the dictionary in which we store errors
    """
    # converting string to dictionary
    response = ast.literal_eval(str(redcap_response))

    try:
        if 'error' in response:
            for recordData in response['records']:
                error_string = "Error writing to record " + recordData["record"] + " field " + recordData[
                    "field_name"] + " Value " + recordData["value"] + ".Error Message: " + recordData["message"]
                logger.error("Handling error in REDCap response: "
                             + error_string)
                form_summary['errors'].append(error_string)
        else:
            logger.error("REDCap response is in unknown format")
    except KeyError as e:
        logger.error("KeyError found while parsing REDCap response: " + str(e))
    return True

"""
create_temp_dir_debug:
Creates a folder name with the following format:
    ./out/out_YYYY_mm_dd:00:11:22
"""


def create_temp_dir_debug(existing_folder=(DEFAULT_DATA_DIRECTORY + 'out')):
    if not os.path.exists(existing_folder):
        try:
            os.makedirs(existing_folder)
        except:
            logger.exception(
                "Folder cannot be created at the path " +
                existing_folder)
            raise
    prefix = 'out_' + datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    mydir = existing_folder + '/' + prefix
    os.mkdir(mydir)
    return mydir

"""
get_temp_path:
This function returns a folder path.
If user enters yes along with the optional command line argument -k, then a folder will be created under project root having a timestamp for its name. The files stored under this folder will not be destroyed.
If user does not use the -k switch then a temporary folder is created at a random location. After the execution of the program, this folder is destroyed.
"""


def get_temp_path(do_keep_gen_files):
    if do_keep_gen_files:
        return create_temp_dir_debug() + '/'
    else:
        return tempfile.mkdtemp('/')

"""
delete_temporary_folder:
deletes the temporary folder specified as argument along with its contents.
"""


def delete_temporary_folder(tmp_folder):
    fileList = os.listdir(tmp_folder)
    for fileName in fileList:
        os.remove(tmp_folder + "/" + fileName)
    try:
        os.rmdir(tmp_folder)
    except OSError:
        logger.exception(
            "Folder " +
            tmp_folder +
            "is not empty, hence cannot be deleted.")
        raise

"""
@see #check_input_file()

The first time we run the app there is no SQLite file
where to store the md5 sums of the input file.
This function creates an empty RediBatch in the SQLite
file specified as `db_path`

@return True if the database file was properly created with an empty table
"""

def create_empty_md5_database(db_path) :
    if os.path.exists(db_path) :
        logger.warn('The file with name ' + db_path + ' already exists')
        #return

    try :
        logger.info('Opening the file:' + db_path)
        fresh_file = open(db_path, 'w')
        fresh_file.close()
        os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)
        time.sleep(5)

    except IOError as e:
        logger.error("I/O error: " + e.strerror + ' for file: ' + db_path)
        return False
    success = create_empty_table(db_path)
    return success

"""
Helper for #create_empty_md5_database()
"""

def create_empty_table(db_path) :
    logger.info('exec create_empty_table')
    db = None
    try:
        db = lite.connect(db_path)
        cur = db.cursor()
        sql = """CREATE TABLE RediBatch (
    rbID INTEGER PRIMARY KEY AUTOINCREMENT,
    rbStartTime TEXT NOT NULL,
    rbEndTime TEXT,
    rbStatus TEXT,
    rbMd5Sum TEXT NOT NULL
)
        """
        cur.execute(sql)

    except lite.Error as e:
        logger.error("SQLite error in create_empty_table(): " + e.args[0])
        return False
    finally:
        if db:
            db.close()
    logger.info('success create_empty_table')
    return True


"""
Use this function to set the `row_factory`
attribute of the database connection
"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

"""
@see bin/redi.py#main()
@return a dictionary representation of the batch row for the current run

Check the md5sum of the input file
    - if the sum *has changed* then continue the data processing and store a row
        in the SQLite database with `batch status= batch_started/ batch_completed`

    - if the sum *did not change* then check the config option `batch_warning_days`:
        - if       limit = -1       then continue execution (ignore the limit)
        - if days_passed > limit    then stop the process and email the `redi_admin`

"""


def check_input_file(batch_warning_days, db_path, email_settings, raw_xml_file):
    batch = None

    if not os.path.exists(db_path) :
        create_empty_md5_database(db_path)

    new_md5ive = get_md5_input_file(raw_xml_file)
    new_msg = 'Using SQLite file: %s to store input file: %s md5 sum: %s' % (
        db_path, raw_xml_file, new_md5ive)
    logger.info(new_msg)

    old_batch = get_last_batch(db_path)
    old_md5ive = None
    if old_batch:
        old_md5ive = old_batch['rbMd5Sum']
        logger.info('Old md5 sum for the input file is: ' + old_md5ive)
    else:
        # this is the first time the checksum feature is used
        logger.info(
            "There is no old md5 recorded yet for the input file. Continue data import...")
        batch = add_batch_entry(db_path, new_md5ive)
        record_msg = 'Added batch (rbID= %s, rbStartTime= %s, rbMd5Sum= %s' % (
            batch['rbID'], batch['rbStartTime'], batch['rbMd5Sum'])
        logger.info(record_msg)
        return batch

    if old_md5ive != new_md5ive:
        # the data has changed... insert a new batch entry
        batch = add_batch_entry(db_path, new_md5ive)
        record_msg = 'Added batch (rbID= %s, rbStartTime= %s, rbMd5Sum= %s' % (
            batch['rbID'], batch['rbStartTime'], batch['rbMd5Sum'])
        logger.info(record_msg)
        return batch
    else:
        days_since_today = get_days_since_today(old_batch['rbStartTime'])
        # TODO: refactor code to use ConfigParser.RawConfigParser in order to
        # preserve data types

        if (days_since_today > int(batch_warning_days)):
            logger.info('Last import was started on: %s which is more than the limit of %s' % (old_batch['rbStartTime'], batch_warning_days))
            if (-1 == int(batch_warning_days)):
                msg_continue = """
                The configuration `batch_warning_days = -1` indicates that we want to continue
                execution even if the input file did not change
                """
                logger.info(msg_continue)
            else:

                msg_quit = "The input file did not change in the past: %s days. Stop data import." % batch_warning_days
                logger.critical(msg_quit)
                redi_email.send_email_input_data_unchanged(email_settings)
                sys.exit()
        else:
            logger.info('Reusing md5 entry: ' + str(old_batch['rbID']))
    # return the old batch so we can update the status
    return old_batch


"""
Retrieve the row corresponding to the last REDI batch completed
"""


def get_last_batch(db_path):
    db = None
    try:
        db = lite.connect(db_path)
        db.row_factory = dict_factory
        cur = db.cursor()
        sql = """
SELECT
    rbID, rbStartTime, rbEndTime, rbMd5Sum
FROM
    RediBatch
ORDER BY rbID DESC
LIMIT 1
"""
        cur.execute(sql)
        batch = cur.fetchone()

    except lite.Error as e:
        logger.error("SQLite error in get_last_batch() for file %s - %s" % (db_path, e.args[0]))
        return None
    finally:
        if db:
            db.close()

    return batch


"""
Retrieve the row corresponding to the specified primary key
"""


def get_batch_by_id(db_path, batch_id):
    db = None
    try:
        db = lite.connect(db_path)
        db.row_factory = dict_factory
        cur = db.cursor()
        sql = """
SELECT
    rbID, rbStartTime, rbEndTime, rbMd5Sum
FROM
    RediBatch
WHERE
    rbID = ?
LIMIT 1
"""
        cur.execute(sql, (str(batch_id), ))
        batch = cur.fetchone()

    except lite.Error as e:
        logger.exception("SQLite error in get_batch_by_id(): %s:" % e.args[0])
        raise
        # sys.exit(1)
    finally:
        if db:
            db.close()

    return batch


"""
@see #check_input_file()
@see https://docs.python.org/2/library/hashlib.html
@see https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory

Returns the md5 sum for the redi input file
"""


def get_md5_input_file(input_file):
    if not os.path.exists(input_file):
        raise Exception('Input file not found at: ' + input_file)

    logger.info('Computing md5 sum for: ' + input_file)

    # open the file in binary mode
    f = open(input_file, 'rb')
    chunk_size = 2 ** 20
    md5 = hashlib.md5()

    # read the input file in 1MB pieces
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        md5.update(chunk)

    return md5.hexdigest()


"""
@see #check_input_file()
@param db_path - the SQLite file
@param md5 - the md5 sum to be inserted
"""


def add_batch_entry(db_path, md5):
    logger.info('Execute: add_batch_entry()')
    batch = None

    db = None
    try:
        db = lite.connect(db_path)
        db.row_factory = dict_factory
        cur = db.cursor()
        sql = """
INSERT INTO RediBatch
    (rbStartTime, rbEndTime, rbStatus, rbMd5Sum)
VALUES
    ( ?, NULL, 'Started', ?)
"""
        now = get_db_friendly_date_time()
        cur.execute(sql, (now, md5))
        rbID = cur.lastrowid
        db.commit()
        batch = get_batch_by_id(db_path, rbID)

    except lite.Error as e:
        logger.error("SQLite error in add_batch_entry() for file %s - %s" % (db_path, e.args[0]))
        return None
    finally:
        if db:
            db.close()

    return batch


"""
Update the status and the finish time of a specified batch entry in the SQLite db

@return True if update succeeded, False otherwise
"""


def update_batch_entry(db_path, id, status, timestamp):
    success = None
    db = None
    try:
        db = lite.connect(db_path)
        cur = db.cursor()
        sql = """
UPDATE
    RediBatch
SET
    rbEndTime = ?
    , rbStatus = ?
WHERE
    rbID = ?
"""

        cur.execute(sql, (timestamp, status, id))
        db.commit()
        scuccess = True
    except lite.Error as e:
        logger.exception("SQLite error in update_batch_entry(): %s:" % e.args[0])
        success = False
    finally:
        if db:
            db.close()

    return success


"""
@return string in format: "2014-06-24 01:23:24"
"""


def get_db_friendly_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

"""
@return string in format: 2014-06-24
"""


def get_db_friendly_date():
    return date.today()

"""
@return the number of days passed since the specified date
"""


def get_days_since_today(date_string):
    num = None
    other = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    delta = now - other
    return delta.days

"""
Helper function for debugging xml content
"""
def printxml(tree):
    print etree.tostring(tree, pretty_print = True)
    return

def get_redcap_client(redcap_settings, email_settings):
    """
    Helper method used to check availability of REDCap
    Warning: will send a warning email and interrupt execution
        if communication with REDCap fails
    """
    try:
        client = redcapClient(
            redcap_settings['redcap_uri'],
            redcap_settings['token'],
            redcap_settings['verify_ssl'])
    except RequestException:
        redi_email.send_email_redcap_connection_error(email_settings)
        raise
    return client

def transfer_pfe_tree(
        pfe_tree,
        redcap_settings,
        email_settings,
        pfe_repo,
        skip_blanks):
    """
    The main method which transfers Person Form Event xml to REDCap
    using #send_person_form_data_to_redcap() function.

    Returns a summary of the transfer success:
        'total_subjects'        : 3,
        'form_details'          : { Total_abc_Forms : 123, ...},
        'subject_details'       : { study_id : { Total_abc_Forms : 123, ... },  ... }
        'errors'                : []
        'subject_details_events : {study_id : event_count, ...}

    Note: `total_subjects` is incremented even if the forms for the subject
        are empty or there was an error while sending the data to REDCap.
    """
    client = get_redcap_client(redcap_settings, email_settings)
    summary = init_summary()

    # Loop through the Person_Form_Event tree and generate
    root = pfe_tree.getroot()
    persons = root.xpath('//person')

    for person in persons:
        summary['total_subjects'] += 1
        study_id = person.get('study_id')
        logger.info('Start sending forms for study_id: ' + study_id)
        forms = person.xpath('./all_form_events/form')

        for form in forms:
            form_name = form.get('form_name')
            fk = FormKey(study_id, form_name)
            form_summary = _send_person_form_data_to_redcap(client, pfe_repo, study_id, form, skip_blanks)
            summary = _update_summary(summary, fk, form_summary)
    logger.debug(summary)
    return summary

def _send_person_form_data_to_redcap(client, pfe_repo, study_id, form, skip_blanks):
    """
    Loop through the events of the given form and build
    the data structure to be sent to REDCap.

    If a form fails to be sent then the entire form
    is added to a list of `unsent` forms which can be
    resent later if needed.
<event>
     <name>1_arm_1</name>
     <field> <name>inr_abc</name> <value>1</value></field>
     <field> <name>inr_xyz</name> <value>2</value></field>
</event>
    """
    form_contains_data = False
    form_name = form.get('form_name')
    logger.debug("sending form `{}`, study_id: `{}` ".format(form_name, study_id))

    # The list of dictionaries representing each event in the form
    form_events_list = []

    for event in form.xpath('event'):
        validate_event(event)
        event_dict = {
            'redcap_event_name': event.find('name').text,
        }

        for field in event.xpath('field'):
            val = get_child_text_safely(field, 'value')
            name = field.findtext('name')
            event_dict[name] = val
            if val and not form_contains_data:
                form_contains_data = True

        event_dict.update({client.project.def_field: study_id})
        form_events_list.append(event_dict)

    if not form_contains_data:
        logging.debug("Form `{}` is empty for study_id `{}`".format(form_name , study_id))

    # Now that the events of this form are parsed send the json data in a batch
    form_summary = _execute_send_data_to_redcap(client,
                                                pfe_repo,
                                                form,
                                                form_contains_data,
                                                form_events_list,
                                                skip_blanks)
    return form_summary

def _execute_send_data_to_redcap(client,
                                pfe_repo,
                                form,
                                form_contains_data,
                                form_events_list,
                                skip_blanks):
    """
    Helper method for _send_person_form_data_to_redcap
    Note: the returned value of this method is parsed by "_update_summary"
    """
    form_summary = {
        'was_sent': True,
        'total_events': 0,
        'errors': [],
    }

    if not form_contains_data and skip_blanks:
        return form_summary

    if form.get('redcap_status'):
        # (!) This is a resumed batch but this form was already sent
        # Return a fake summary so the report includes total counts
        logger.debug("Skip sending already sent form: " + form.get('form_name'))
        fake_summary = {
            'was_sent': True,
            'total_events': len(form_events_list),
        }
        return fake_summary

    found_error = False
    try:
        response = client.send_data_to_redcap(form_events_list, overwrite = True)
        # If the form was sent to REDCap update add an extra attribute
        # which is later used for the resuming
        form.set('redcap_status', redi.STATUS_SENT)
        form_tree = etree.ElementTree(form)
        pfe_repo.store(form_tree)
    except RedcapError as e:
        found_error = handle_errors_in_redcap_xml_response(e.message, form_summary)
    if not found_error:
        form_summary['was_sent'] = True
        form_summary['total_events'] = len(form_events_list)
    return form_summary

def init_summary():
    """
    Called by `transfer_pfe_tree` to initialize the data structure passed to `_update_summary`
    """
    return {
        'total_subjects' : 0,
        'form_details'   : {},
        'subject_details': {},
        'errors'         : [],
        'subject_events' : collections.defaultdict(int),
    }

def _update_summary(summary, fk, form_summary):
    """
    Receives status data about one form transfer to REDCap.
    The returned `summary` dictionary is passed later on to the function
    which create an html report of the entire batch.
    Note: `fk` is an instance of the FormKey class and it is used to decide
    where to `merge` the `form_summary` data.
    """
    total_key = fk.get_total_key()

    # form_details
    if total_key not in summary['form_details']:
        summary['form_details'][total_key] = 0

    if "was_sent" in form_summary:
        summary['form_details'][total_key] += 1

    # subject_details
    if fk.study_id not in summary['subject_details']:
        summary['subject_details'][fk.study_id] = {}

    if total_key not in summary['subject_details'][fk.study_id]:
        summary['subject_details'][fk.study_id][total_key] = 0

    if "was_sent" in form_summary and form_summary['was_sent']:
        summary['subject_details'][fk.study_id][total_key] += 1

    # errors
    if form_summary['errors']:
        summary['errors'].append(form_summary['errors'])

    # event counts
    # TODO: add column in the report: study_id -> total_events parsed
    summary['subject_events'][fk.study_id] += form_summary['total_events']
    return summary

def validate_event(event):
    """ @see send_person_form_data_to_redcap"""
    event_name = event.find('name')
    if event_name is None or not event_name.text:
        raise Exception('Expected non-blank element event/name')

    event_field_name_list = event.xpath('field/name')

    for name in event_field_name_list:
        if name.text is None:
            raise Exception(
                'Expected non-blank element event/field/name')

class FormKey:
    def __init__(self, study_id, form_name):
        self.study_id = study_id
        self.form_name = form_name

    def get_total_key(self):
        return "Total_" + self.form_name + "_Forms"

