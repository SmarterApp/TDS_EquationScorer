###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

import unittest
from xml.etree import ElementTree as et
import logging

from airscore.mathmlsympy.parser import MathmlBuilder
XML_1 = u"""
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
 <mstyle displaystyle="true">
  <mn>1</mn><mi>x</mi><mo>\u2264</mo><mn>3</mn>
 </mstyle>
</math>
""".encode('UTF-8')

XML_2 = u"""
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
 <mstyle displaystyle="true">
  <mo>(</mo><mn>5</mn><mo>.</mo><mn>0</mn><mo>)</mo>
 </mstyle>
</math>""".encode('UTF-8')

MATHML_TEMPLATE=u"""
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mstyle displaystyle="true">{}</mstyle></math>
"""


LOGGER=logging.getLogger()

class TestCase( unittest.TestCase ):
    
    @property
    def parser(self):
        return et.XMLParser( target = MathmlBuilder(), encoding="UTF-8" )
        
    @staticmethod
    def mathml_wrap( exp ):
        return MATHML_TEMPLATE.format( exp ).encode( 'UTF-8' )
    