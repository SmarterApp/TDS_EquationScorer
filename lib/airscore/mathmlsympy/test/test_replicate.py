########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

import os
from xml.etree import ElementTree as et

import abstract_parser_test
from airscore.mathmlsympy.parser import process_mathml_data

TEST_DIR = os.path.dirname( __file__ )
RESPONSE_FILE = "responses.xhtml"

class Test(abstract_parser_test.TestCase):

    def testReplicate(self):
        input_doc = et.parse(os.path.join( TEST_DIR, RESPONSE_FILE ) )
        succeed = 0
        fail = 0
        for tr in input_doc.findall( u'*//{http://www.w3.org/1999/xhtml}table/{http://www.w3.org/1999/xhtml}tr' ):
            mathml_node = tr[0][0]
            mathml_string = et.tostring( mathml_node, 'UTF-8' )
            expected = tr[1].text.encode( 'UTF-8' )
            found = str( process_mathml_data( mathml_string ) )
            if expected == found:
                abstract_parser_test.LOGGER.debug( u"Match for {}: {}=={}".format( mathml_string, expected, found ) )
                succeed += 1
            else:
                abstract_parser_test.LOGGER.error( u"For {}:\n  expected {},\n     found {}\n".format( mathml_string, expected, found ) )
                fail += 1
        self.assertFalse( fail, 
            abstract_parser_test.LOGGER.error( u"Replication failed {} times, succeeded {} times".format( fail, succeed ) )
            )
