import unittest
from lxml import etree
import os
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestUpdateStatusField(unittest.TestCase):

  def test_update_status_field_value_when_one_subject_with_two_forms_with_one_event_in_each_form(self):
    redi.configure_logging(DEFAULT_DATA_DIRECTORY)
    self.source = """<person_form_event>
      <person>
          <study_id>99</study_id>
          <all_form_events>
              <form>
                  <name>cbc</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value/>
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value>500</value>
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value/>
                      </field>
                  </event>
              </form>
              <form>
                  <name>inr</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value/>
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value/>
                      </field>
                  </event>
              </form>
          </all_form_events>
      </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
      <person>
          <study_id>99</study_id>
          <all_form_events>
              <form>
                  <name>cbc</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value/>
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value>500</value>
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value/>
                      </field>
                  </event>
              </form>
              <form>
                  <name>inr</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value/>
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value>NOT_DONE</value>
                      </field>
                  </event>
              </form>
          </all_form_events>
      </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def test_update_status_field_value_when_one_subject_with_two_forms_with_two_events_in_each_form(self):
    redi.configure_logging(proj_root+'log/redi.log')
    self.source = """<person_form_event>
      <person>
          <study_id>99</study_id>
          <all_form_events>
              <form>
                  <name>cbc</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value/>
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value>500</value>
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value/>
                      </field>
                  </event>
                  <event>
                      <name>1_arm_2</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value/>
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value/>
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value/>
                      </field>
                  </event>
              </form>
              <form>
                  <name>inr</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value/>
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value/>
                      </field>
                  </event>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value>2</value>
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value/>
                      </field>
                  </event>
              </form>
          </all_form_events>
      </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
      <person>
          <study_id>99</study_id>
          <all_form_events>
              <form>
                  <name>cbc</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value />
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value>500</value>
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value />
                      </field>
                  </event>
                  <event>
                      <name>1_arm_2</name>
                      <field>
                          <name>cbc_lbdtc</name>
                          <value>1905-10-01</value>
                      </field>
                      <field>
                          <name>wbc_lborres</name>
                          <value>3.0</value>
                      </field>
                      <field>
                          <name>wbc_lbstat</name>
                          <value />
                      </field>
                      <field>
                          <name>neut_lborres</name>
                          <value />
                      </field>
                      <field>
                          <name>neut_lbstat</name>
                          <value />
                      </field>
                  </event>
              </form>
              <form>
                  <name>inr</name>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value />
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value>NOT_DONE</value>
                      </field>
                  </event>
                  <event>
                      <name>1_arm_1</name>
                      <field>
                          <name>inr_lbdtc</name>
                          <value>1906-12-01</value>
                      </field>
                      <field>
                          <name>inr_lborres</name>
                          <value>2</value>
                      </field>
                      <field>
                          <name>inr_lbstat</name>
                          <value />
                      </field>
                  </event>
              </form>
          </all_form_events>
      </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def test_update_status_field_value_when_two_subjects_with_two_forms_with_one_event_in_each_form(self):
    redi.configure_logging(proj_root+'log/redi.log')
    self.source = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>cbc_lbdtc</name>
                              <value>1905-10-01</value>
                          </field>
                          <field>
                              <name>wbc_lborres</name>
                              <value>3.0</value>
                          </field>
                          <field>
                              <name>wbc_lbstat</name>
                              <value/>
                          </field>
                          <field>
                              <name>neut_lborres</name>
                              <value>500</value>
                          </field>
                          <field>
                              <name>neut_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>cbc_lbdtc</name>
                              <value>1905-10-01</value>
                          </field>
                          <field>
                              <name>wbc_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>wbc_lbstat</name>
                              <value/>
                          </field>
                          <field>
                              <name>neut_lborres</name>
                              <value>500</value>
                          </field>
                          <field>
                              <name>neut_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value>2</value>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>cbc_lbdtc</name>
                              <value>1905-10-01</value>
                          </field>
                          <field>
                              <name>wbc_lborres</name>
                              <value>3.0</value>
                          </field>
                          <field>
                              <name>wbc_lbstat</name>
                              <value/>
                          </field>
                          <field>
                              <name>neut_lborres</name>
                              <value>500</value>
                          </field>
                          <field>
                              <name>neut_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value>NOT_DONE</value>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>cbc_lbdtc</name>
                              <value>1905-10-01</value>
                          </field>
                          <field>
                              <name>wbc_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>wbc_lbstat</name>
                              <value>NOT_DONE</value>
                          </field>
                          <field>
                              <name>neut_lborres</name>
                              <value>500</value>
                          </field>
                          <field>
                              <name>neut_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value>2</value>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def test_update_status_field_value_when_one_subject_with_no_form(self):
    redi.configure_logging(proj_root+'log/redi.log')
    self.source = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
              </all_form_events>
          </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
              </all_form_events>
          </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def test_update_status_field_value_when_one_subject_with_two_forms_event_missing_in_one_of_the_forms(self):
    redi.configure_logging(proj_root+'log/redi.log')
    self.source = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>cbc</name>
                  </form>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                              <value/>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value>NOT_DONE</value>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def test_update_status_field_value_when_one_subject_with_one_form_one_event_value_tag_missing(self):
    redi.configure_logging(proj_root+'log/redi.log')
    self.source = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value/>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
      """

    self.source_tree = etree.ElementTree(etree.fromstring(self.source))

    self.input = """
    <rediFieldMap>
      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
          <redcapStatusFieldName>wbc_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>cbc</redcapFormName>
          <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
          <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
      </clinicalComponent>

      <clinicalComponent>
          <redcapFormName>inr</redcapFormName>
          <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
          <redcapStatusFieldName>inr_lbstat</redcapStatusFieldName>
          <redcapStatusFieldValue>NOT_DONE</redcapStatusFieldValue>
      </clinicalComponent>
      </rediFieldMap>
    """

    self.input_tree = etree.ElementTree(etree.fromstring(self.input))

    self.output = """<person_form_event>
          <person>
              <study_id>99</study_id>
              <all_form_events>
                  <form>
                      <name>inr</name>
                      <event>
                          <name>1_arm_1</name>
                          <field>
                              <name>inr_lbdtc</name>
                              <value>1906-12-01</value>
                          </field>
                          <field>
                              <name>inr_lborres</name>
                          </field>
                          <field>
                              <name>inr_lbstat</name>
                              <value>NOT_DONE</value>
                          </field>
                      </event>
                  </form>
              </all_form_events>
          </person>
      </person_form_event>
    """
    self.expect = etree.tostring(etree.fromstring(self.output))
    redi.updateStatusFieldValueInPersonFormEventTree(self.source_tree, self.input_tree)
    result = etree.tostring(self.source_tree)
    self.assertEqual(self.expect, result)

  def tearDown(self):
    return()

if __name__ == "__main__":
    unittest.main()
