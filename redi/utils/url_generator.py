# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

import logging
from HTMLParser import HTMLParser
import urllib
import urllib2
"""
Usage:
    Below is the sample code to use this utility.

    from url_generator import url_generator

    url = "http://localhost:8998/redcap/plugins/show_url.php"
    values = {"project_name":"Classic Database",
              "study_id":"999-001",
              "page_name":"demographics",
              "event_name":"Event 1"}
    parser = InitPlugin(url, values)


"""
# Configure module's logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class InitPlugin():
    """Call the Form URL Plugin for REDCap with POST parameters
    and get the response.
    Parse the response and extract the URL form it.

    """
    def __init__(self, url, values):
        self.url = url
        self.values = values
        log_str = "Initializing Plugin parser with URL: "+self.url
        logger.info(log_str)
        self.get_response(self.url, self.values)

    def get_response(self, url, values):
        post_data = urllib.urlencode(values)
        prepared_request = urllib2.Request(url, post_data)
        response = urllib2.urlopen(prepared_request)
        html_string = response.read()
        parser = PluginParser()
        parser.feed(html_string)
        return parser.output

class PluginParser(HTMLParser):
    """Parser module for the HTML response received

    """
    def feed(self, data):
        self.output = []
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        # search for tag 'a'
        if tag == "a":
            # iterate through properties of anchor tag
            for name, value in attrs:
                if name == "href":
                    self.output.append(value)
