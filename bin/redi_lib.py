#/usr/bin/env python

"""
redi_lib.py

    Stores a collection of utility functions used by redi.py
"""

__author__      = "University of Florida CTS-IT Team"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 2-Clause"

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
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
proj_root = redi.get_proj_root()


# Constants
DEFAULT_RATE_LIMITER = 600
DEFAULT_BATCH_WARNING_DAYS = 13

"""
create_import_data_json:
This function converts data in event tree into json format.
Parameters:
    import_data_dict: This parameter holds the event tree data
    event_tree: This parameter holds the event tree data

@see #generate_output()
"""


def create_import_data_json(
        import_data_dict,
        event_tree):
    # redi.configure_logger(system_log_file_full_path)

    root = event_tree

    event_name = root.find('name')
    if event_name is None or not event_name.text:
        raise Exception('Expected non-blank element event/name')

    import_data_dict['redcap_event_name'] = event_name.text

    event_field_value_list = root.xpath('//event/field/name')

    for name in event_field_value_list:
        if name.text is None:
            raise Exception(
                'Expected non-blank element event/field/name')

    # Match all fields to build a row for each
    event_field_list = root.xpath('field')
    contains_data = False

    for field in event_field_list:
        val = get_child_text_safely(field, 'value')
        import_data_dict[field.findtext('name')] = val

        if val and not contains_data:
            contains_data = True

    return {'json_data': import_data_dict, 'contains_data': contains_data}

"""
Convenience function
@see create_eav_output
"""


def get_child_text_safely(etree, ele):
    ele = etree.find(ele)
    if ele.text is None:
        return ''
    else:
        return ele.text

"""
Note: This function communicates with the redcap application.
Steps:
    - loop for each person/form/event element
    - generate a csv fragment `using create_eav_output`
    - send csv fragment to RedCap using `send_eav_data_to_redcap`


@return the report_data dictionary
"""


def generate_output(person_tree, settings):
    # redi.configure_logger(system_log_file_full_path)

    # the global dictionary to be returned
    report_data = {
        'errors': []
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

    root = person_tree.getroot()
    persons = root.xpath('//person')

    redcapClientObject = redcapClient(settings)    

    if (not settings.hasoption('rate_limiter_value_in_redcap') or '' == settings.rate_limiter_value_in_redcap) :
        rate_limiter_value_in_redcap = DEFAULT_RATE_LIMITER
        logger.warn("Missing parameter 'rate_limiter_value_in_redcap' in settings.ini.")
        logger.warn("Using default value: rate_limiter_value_in_redcap = " + str(DEFAULT_RATE_LIMITER))
    else :
        rate_limiter_value_in_redcap = float(settings.rate_limiter_value_in_redcap)


    ideal_time_per_request = 60 / float(rate_limiter_value_in_redcap)
    time_stamp_after_request = 0

    # main loop for each person
    for person in persons:
        time_begin = datetime.datetime.now()
        person_count += 1
        study_id = (person.xpath('study_id') or [None])[0]

        if study_id is None:
            raise Exception('Expected a valid value for study_id')

        # count how many csv fragments are created per person
        event_count = 0
        logger.info('Start sending data for study_id: %s' % study_id.text)

        forms = person.xpath('./all_form_events/form')

        # loop through the forms of one person
        for form in forms:
            form_name = form.xpath('name')[0].text
            form_key = 'Total_' + form_name + '_Forms'
            study_id_key = study_id.text

            # init dictionary for a new person in (study_id)
            if study_id_key not in subject_details:
                subject_details[study_id_key] = {}

            if not form_key in subject_details[study_id_key]:
                subject_details[study_id_key][form_key] = 0

            if form_key not in form_details:
                form_details[form_key] = 0

            logger.debug(
                'parsing study_id ' +
                study_id.text +
                ' form: ' +
                form_name)

            # loop through the events of one form
            for event in form.xpath('event'):
                event_count += 1

                try:
                    import_dict = {
                        redcapClientObject.project.def_field: study_id.text}
                    import_dict = create_import_data_json(
                        import_dict,
                        event)
                    json_data_dict = import_dict['json_data']
                    contains_data = import_dict['contains_data']

                    time_lapse_since_last_request = time.time(
                    ) - time_stamp_after_request
                    sleepTime = max(
                        ideal_time_per_request -
                        time_lapse_since_last_request,
                        0)
                    # print 'Sleep for: %s seconds' % sleepTime
                    time.sleep(sleepTime)

                    if (0 == event_count % 50):
                        logger.info('Requests sent: %s' % (event_count))

                    # to speedup testing uncomment the following line
                    # if (0 == event_count % 2) : continue

                    try:
                        found_error = False
                        response = redcapClientObject.send_data_to_redcap([json_data_dict], overwrite = True)
                    except RedcapError as e:
                        found_error = handle_errors_in_redcap_xml_response(
                            e.message,
                            report_data)

                    time_stamp_after_request = time.time()

                    if contains_data:
                        if not found_error:
                            # if no errors encountered update event counters
                            subject_details[study_id_key][form_key] += 1
                            form_details[form_key] += 1

                except Exception as e:
                    logger.error(e.message)
                    raise

        time_end = datetime.datetime.now()
        logger.info("Total execution time for study_id %s was %s" % (study_id_key, (time_end - time_begin)))
        logger.info("Total REDCap requests sent: %s \n" % (event_count))

    report_data.update({
        'total_subjects': person_count,
        'form_details': form_details,
        'subject_details': subject_details,
        'errors': report_data['errors']
    })

    logger.debug('report_data ' + repr(report_data))
    return report_data

"""
handle_errors_in_redcap_xml_response:
This function checks for any errors in the redcap response and update report data if there are any errors.
Parameters:
    redcap_response_xml: This parameter holds the redcap response passed to this function
    report_data: This parameter holds the report data passed to this function
    
"""


def handle_errors_in_redcap_xml_response(redcap_response, report_data):
    # converting string to dictionary
    response = ast.literal_eval(str(redcap_response))
    logger.info('handling response from the REDCap')
    try:
        if 'error' in response:
            for recordData in response['records']:
                error_string = "Error writing to record " + recordData["record"] + " field " + recordData[
                    "field_name"] + " Value " + recordData["value"] + ".Error Message: " + recordData["message"]
                logger.info(error_string)
                report_data['errors'].append(error_string)
        else:
            logger.error("REDCap response is in unknown format")
    except KeyError as e:
        logger.error(str(e))
    return True


# Convenience method for getting the first element
# Note: for printing an object can use: print  repr(obj)
def get_first_item(aList):
    if aList:
        return aList[0]
    return None

"""
create_temp_dir_debug:
Creates a folder name with the following format:
    ./out/out_YYYY_mm_dd:00:11:22
"""


def create_temp_dir_debug(existing_folder=(proj_root + 'out')):
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


def check_input_file(settings, raw_xml_file):
    batch = None

    db_path = redi.get_db_path(settings)

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

    if (old_md5ive != new_md5ive):
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
        if (not settings.hasoption('batch_warning_days') or '' == settings.batch_warning_days) :
            batch_warning_days = DEFAULT_BATCH_WARNING_DAYS
            logger.warn("Missing parameter 'batch_warning_days' in settings.ini.")
            logger.warn("Using default value: batch_warning_days = " + str(DEFAULT_BATCH_WARNING_DAYS))
        else:
            batch_warning_days = settings.batch_warning_days

        if (days_since_today > int(batch_warning_days)):
            logger.info('Last import was started on: %s which is more than the limit of %s' % (old_batch['rbStartTime'], batch_warning_days))
            if (-1 == int(batch_warning_days)):
                msg_continue = """
                The configuration `batch_warning_days = -1` indicates that we want to continue
                execution even if the input file did not change
                """
                loggging.info(msg_continue)
            else:

                msg_quit = "The input file did not change in the past: %s days. Stop data import." % batch_warning_days
                loggging.warn(msg_quit)
                redi_email.send_email_input_data_unchanged(settings)
                quit()
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


if __name__ == "__main__":
    main()
