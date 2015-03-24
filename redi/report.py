# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

import abc
import time

import pkg_resources
from datetime import datetime, timedelta
from lxml import etree

from utils import redi_email

REDI_PACKAGE_NAME = 'redi'


class ReportCourier(object):
    @abc.abstractmethod
    def deliver(self, report):
        raise NotImplementedError()


class ReportFileWriter(ReportCourier):
    def __init__(self, output_file, logger):
        self._output_file = output_file
        self._logger = logger

    def deliver(self, report):
        """
        Deliver the summary report by writing it to a file
        or logging it to the console if writing the file fails

        :html_report_path the path where the report will be stored
        :html the actual report content
        """
        logger = self._logger
        html_report_path = self._output_file
        html = report

        problem_found = False
        try:
            report_file = open(html_report_path, 'w')
        except (IOError, OSError) as e:
            logger.exception('Could not open file: %s' % html_report_path)
            problem_found = True
        else:
            try:
                report_file.write(html)
                logger.info("==> You can review the summary report by opening: {}"\
                    " in your browser".format(html_report_path))
            except IOError:
                logger.exception('Could not write file: %s' % html_report_path)
                problem_found = True
            finally:
                report_file.close()
        if problem_found:
            logger.info("== Summary report ==" + html)


class ReportEmailSender(ReportCourier):
    def __init__(self, settings, logger):
        self._settings = settings
        self._logger = logger

    def deliver(self, report):
        """
        Deliver summary report as an email

        :email_settings dictinary with email parameters
        :html the actual report content
        """
        logger = self._logger
        email_settings = self._settings
        html = report
        # TODO: Replace this with a "backup_courier" constructor injection
        deliver_report_as_file = self.__backup_courier_wrapper()

        try:
            redi_email.send_email_data_import_completed(email_settings, html)
            logger.info("Summary report was emailed: parameter 'send_email = Y'")
        except Exception as e:
            logger.error("Unable to deliver the summary report due error: %s" % e)
            deliver_report_as_file("report.html", html)

    def __backup_courier_wrapper(self):
        # Needed for backwards-compatibility with the old
        # deliver_report_by_file() call from deliver_report_by_email()
        logger = self._logger

        def wrapper(filename, report):
            return ReportFileWriter(filename, logger).deliver(report)

        return wrapper


class ReportCreator(object):
    def __init__(self, report_file_path, project_name, redcap_uri,
                 sort_by_lab_id, writer):
        self._report_parameters = {
            'report_file_path': report_file_path,
            'project': project_name,
            'redcap_uri': redcap_uri,
            'is_sort_by_lab_id': sort_by_lab_id
        }
        self._writer = writer

    def create_report(self, report_data, alert_summary, collection_date_summary_dict, duration_dict):
        report_parameters = self._report_parameters
        write_element_tree_to_file = self._writer

        root = etree.Element("report")
        root.append(etree.Element("header"))
        root.append(etree.Element("summary"))
        root.append(etree.Element("alerts"))
        root.append(etree.Element("subjectsDetails"))
        root.append(etree.Element("errors"))
        root.append(etree.Element("summaryOfSpecimenTakenTimes"))
        updateReportHeader(root, report_parameters)
        updateReportSummary(root, report_data)
        updateSubjectDetails(root, report_data['subject_details'])
        updateReportAlerts(root, alert_summary)
        updateReportErrors(root, report_data['errors'])
        updateSummaryOfSpecimenTakenTimes(root, collection_date_summary_dict)

        # TODO: remove dependency on the order of the xml elements in the report
        sort_by_value = 'lab_id' if report_parameters['is_sort_by_lab_id'] else 'redcap_id'
        root.append(gen_ele("sort_details_by", sort_by_value))

        start = duration_dict['all']['start']
        end = duration_dict['all']['end']
        diff = self.get_time_diff(end, start)
        root.append(gen_ele('time_all_start', start[-8:]))
        root.append(gen_ele('time_all_end', end[-8:]))
        root.append(gen_ele('time_all_diff', self.format_seconds_as_string(diff)))

        tree = etree.ElementTree(root)
        write_element_tree_to_file(tree,report_parameters.get('report_file_path'))

        report_xsl = pkg_resources.resource_filename(REDI_PACKAGE_NAME,
                                                     'utils/report.xsl')
        xslt = etree.parse(report_xsl)
        transform = etree.XSLT(xslt)
        html_report = transform(tree)
        html_str = etree.tostring(html_report, method='html', pretty_print=True)

        return html_str

    def get_time_diff(self, end, start):
        """
        Get time difference in seconds from the two dates
        Parameters
        ----------
        end : string
            The end timestamp
        start : string
            The start timestamp
        """
        # sqlite: select strftime('%s', rbEndTime) - strftime('%s', rbStartTime) from RediBatch;
        fmt = '%Y-%m-%d %H:%M:%S'
        dt_end = datetime.strptime(end, fmt)
        dt_start = datetime.strptime(start, fmt)
        diff = (dt_end - dt_start).total_seconds()
        return diff


    def format_seconds_as_string(self,seconds):
        """
        Convert seconds to a friendly strings
            3662  ==> '01:01:02'
            89662 ==> '1 day, 0:54:22'
        Parameters
        ----------
        seconds : integer
            The number of seconds to be converted
        """
        return str(timedelta(seconds=seconds))


def updateReportHeader(root, report_parameters):
    """ Update the passed `root` element tree with date, project name and url"""
    header = root[0]
    project = etree.SubElement(header, "project")
    project.text = report_parameters.get('project')
    date = etree.SubElement(header, "date")
    date.text = time.strftime("%m/%d/%Y")
    redcapServerAddress = etree.SubElement(header, "redcapServerAddress")
    redcapServerAddress.text = report_parameters.get('redcap_uri')


def updateReportSummary(root, report_data):
    summary = root[1]
    subjectCount = etree.SubElement(summary, "subjectCount")
    subjectCount.text = str(report_data.get('total_subjects'))
    forms = etree.SubElement(summary, "forms")
    form_data = report_data['form_details']
    for k in sorted(form_data.keys()):
        form = etree.SubElement(forms, "form")
        name_element = etree.SubElement(form, "form_name")
        name_element.text = k
        count_element = etree.SubElement(form, "form_count")
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


def updateSubjectDetails(root, subject_details):
    """
    Helper method for #create_summary_report()
    Adds subject information to the xml tree which is later formated
    by `redi/utils/report.xsl` into the html `table#subject_details"`
    """
    subjectsDetails = root[3]
    for key in sorted(subject_details.keys()):
        subject = etree.SubElement(subjectsDetails, "subject")
        details = subject_details.get(key)
        subject.append(gen_ele("redcap_id", key))
        forms = etree.SubElement(subject, "forms")

        for k in sorted(details.keys()):
            if(k.endswith("_Forms")):
                form = etree.SubElement(forms, "form")
                name_element = etree.SubElement(form, "form_name")
                name_element.text = k
                count_element = etree.SubElement(form, "form_count")
                count_element.text = str(details.get(k))
            else:
                element = etree.SubElement(subject, k)
                element.text = str(details.get(k))


def updateReportErrors(root, errors):
    errorsRoot = root[4]
    for error in errors:
        errorElement = etree.SubElement(errorsRoot, "error")
        errorElement.text = str(error)


def updateSummaryOfSpecimenTakenTimes(root, collection_date_summary_dict):
    timeSummaryRoot = root[5]
    totalElement = etree.SubElement(timeSummaryRoot, "total")
    totalElement.text = str(collection_date_summary_dict['total'])
    blankElement = etree.SubElement(timeSummaryRoot, "blank")
    blankElement.text = str(collection_date_summary_dict['blank'])
    percentElement = etree.SubElement(timeSummaryRoot, "percent")
    percentElement.text = str((float(collection_date_summary_dict['blank'])/\
        collection_date_summary_dict['total'])*100)


def gen_ele(ele_name, ele_text):
    """ Create an xml element with given name and content """
    return etree.XML("<{}>{}</{}>".format(ele_name, ele_text, ele_name))


def gen_subele(parent, subele_name, subele_text):
    subele = etree.SubElement(parent, subele_name)
    subele.text = subele_text
    return subele
