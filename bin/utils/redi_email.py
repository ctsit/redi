import smtplib
from smtplib import SMTPException
import logging

def send_email_redcap_connection_error(email_settings, subject='', msg=''):
    sender = email_settings['redcap_support_sender_email']


    receiver = email_settings['redcap_support_receiver_email'].split()
    host = email_settings['smtp_host_for_outbound_mail']
    port = email_settings['smtp_port_for_outbound_mail']
    subject = 'Communication failure: Unable to reach REDCap instance'
    msg = 'A problem was encountered when connecting to the REDCap. Please investigate if REDCap is running.'

    send_email(host, str(port), sender, receiver, None, subject, msg)
    logging.error('Exception: Unable to communicate with REDCap instance at: ' + email_settings['redcap_uri'])



"""
    Send a warning email to the `redcap_support_receiver_email`
    if the input file did not change for more than `batch_warning_days`
"""


def send_email_input_data_unchanged(email_settings, subject='', msg=''):
    sender = email_settings['redcap_support_sender_email']
    receiver = email_settings['redcap_support_receiver_email'].split()
    host = email_settings['smtp_host_for_outbound_mail']
    port = email_settings['smtp_port_for_outbound_mail']
    subject = 'Input data is static.'
    msg = 'Administrators, \n For the past %s days the input data for the REDI application did not change. Please investigate.' % email_settings['batch_warning_days']
    send_email(host, str(port), sender, receiver, None, subject, msg)


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
