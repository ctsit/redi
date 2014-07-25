import unittest
from lxml import etree
from form import Form


class TestEventIsEmpty(unittest.TestCase):
    def test_is_empty(self):
        raw_xml = """
            <person_form_event>
              <person>
                <study_id>60</study_id>
                <all_form_events>
                  <form>
                    <name>hcv_rna_results</name>
                    <event>
                      <name>1_arm_1</name>
                      <field><name/><value/></field>
                      <field><name>hcv_lbdtc</name><value/></field>
                    </event>
                  </form>
                </all_form_events>
              </person>
            </person_form_event>"""

        form = Form(etree.fromstring(raw_xml))
        event = form.events().next()

        self.assertTrue(event.is_empty())

    def test_is_not_empty(self):
        raw_xml = """
            <person_form_event>
              <person>
                <study_id>60</study_id>
                <all_form_events>
                  <form>
                    <name>hcv_rna_results</name>
                    <event>
                      <name>1_arm_1</name>
                      <field><name/><value>o hai</value></field>
                      <field><name>hcv_lbdtc</name><value/></field>
                    </event>
                  </form>
                </all_form_events>
              </person>
            </person_form_event>"""

        form = Form(etree.fromstring(raw_xml))
        event = form.events().next()

        self.assertFalse(event.is_empty())


if __name__ == "__main__":
    unittest.main()
