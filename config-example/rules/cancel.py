__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"

######################################################
#
#
#  Cancel.py module
#       This module looks for 'CANCELED', 'CANCELLED'
#       or other variations and blanks out the form
#       before sending to REDCap.
#
#
######################################################

from form import Form
import re


def run_rules(data):
    """Mandatory function which runs the rules pertaining
        to this module

    """
    form = Form(data)
    for event in form.events():
        for field in event.fields():
            field_value = field.value
            if not field_value:
                continue
            else:
                is_cancelled = False
                is_cancelled = process_field_cancelled_value(field_value)
                if is_cancelled is True:
                    # clear the field value
                    field.clear_value()
                else:
                    continue
    return form

def process_field_cancelled_value(value):
    """This method processes the value in field. It checks
        for the value 'CANCELED' or 'CANCELLED' in the
        <value> tag under the parent <field> tag.
    """
    value = value.strip().lower()
    cancel_match = re.findall(r'cancel[led$]*', value, re.I)
    if not cancel_match:
        return False
    else:
        return True
