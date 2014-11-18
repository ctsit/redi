"""
Functions related to the RediBatch database
"""

__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"

import datetime
import hashlib
import logging
import os
import sqlite3 as lite
import stat
import sys
import time

from lxml import etree

from utils import redi_email
from utils.rawxml import RawXml


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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


def check_input_file(batch_warning_days, db_path, email_settings, raw_xml_file, project):
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
            raw_xml = RawXml(project, raw_xml_file)
            msg_file_details = "\nXML file details: " + raw_xml.get_info()
            logger.info('Last import was started on: %s which is more than the limit of %s' % (old_batch['rbStartTime'], batch_warning_days))
            if (-1 == int(batch_warning_days)):
                msg_continue = """
                The configuration `batch_warning_days = -1` indicates that we want to continue
                execution even if the input file did not change
                """ + msg_file_details
                logger.info(msg_continue)
            else:

                msg_quit = "The input file did not change in the past: %s days. Stop data import." % batch_warning_days
                logger.critical(msg_quit + msg_file_details)
                redi_email.send_email_input_data_unchanged(email_settings, raw_xml)
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
    return datetime.date.today()

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
