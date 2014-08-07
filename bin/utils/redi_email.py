import smtplib
from smtplib import SMTPException
import logging

DEFAULT_REDCAP_SUPPORT_SENDER_EMAIL = "please-do-not-reply@ufl.edu"

def send_email_redcap_connection_error(settings, subject='', msg=''):
    if not settings.hasoption('redcap_support_sender_email'):
        sender = DEFAULT_REDCAP_SUPPORT_SENDER_EMAIL
        logging.warn("Missing parameter redcap_support_sender_email in settings.ini")
        logging.warn("Using default value: redcap_support_sender_email = " + DEFAULT_REDCAP_SUPPORT_SENDER_EMAIL)
    else:
        sender = settings.redcap_support_sender_email

    receiver = settings.redcap_support_receiver_email.split()
    host = settings.smtp_host_for_outbound_mail
    port = settings.smtp_port_for_outbound_mail
    subject = 'Communication failure: Unable to reach REDCap instance'
    msg = 'A problem was encountered when connecting to the REDCap. Please investigate if REDCap is running.'

    send_email(host, str(port), sender, receiver, None, subject, msg)
    logging.error('Exception: Unable to communicate with REDCap instance at: ' + settings.redcap_uri)

    quit()
    return

"""
    Send a warning email to the `redcap_support_receiver_email`
    if the input file did not change for more than `batch_warning_days`
"""


def send_email_input_data_unchanged(settings, subject='', msg=''):
    if not settings.hasoption('redcap_support_sender_email'):
        sender = DEFAULT_REDCAP_SUPPORT_SENDER_EMAIL
        logging.warn("Missing parameter redcap_support_sender_email in settings.ini")
        logging.warn("Using default value: redcap_support_sender_email = " + DEFAULT_REDCAP_SUPPORT_SENDER_EMAIL)
    else:
        sender = settings.redcap_support_sender_email

    receiver = settings.redcap_support_receiver_email.split()
    host = settings.smtp_host_for_outbound_mail
    port = settings.smtp_port_for_outbound_mail
    subject = 'Input data is static.'
    msg = 'Administrators, \n For the past %s days the input data for the REDI application did not change. Please investigate.' % settings.batch_warning_days

    send_email(host, str(port), sender, receiver, None, subject, msg)
    logging.error('Exception: Unable to communicate with REDCap instance at: ' + settings.redcap_uri)

    return


def send_email(
        host,
        port,
        sender,
        to_addr_list,
        cc_addr_list,
        subject,
        msg_body):
    #print ('host %s, port: %s' % (host, port))
    try:
        smtp = smtplib.SMTP(host, port)
        header = 'From: %s\n' % sender
        header += 'To: %s\n' % ','.join(to_addr_list)
        if cc_addr_list:
            header += 'Cc: %s\n' % ','.join(cc_addr_list)
        if subject:
            header += 'Subject: %s\n\n' % subject
        msg = header + msg_body
        smtp.sendmail(sender, to_addr_list, msg)
        logging.info(
            'Success: Email with subject [' +
            subject +
            '] was sent to:' +
            str(to_addr_list))
    except SMTPException:
        logging.warn("Error: Unable to send email to " + to_addr_list)
    return
