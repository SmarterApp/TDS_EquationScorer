#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from parser import mathml_element
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import PartialSympyObject, SYMPY_NONE

FUNCTION_NAMES = set( ( u"sin", u"cos", u"tan", u"asin", u"acos", u"atan", u"log", u"ln", u"exp", u"f", u"g" ) )

@mathml_element( 'mi', 'mtext' )
class MathmlMI( BaseMathmlElement ):
    def pick_subclass( self ):
        if self.decoded_text in FUNCTION_NAMES:
            self.__class__ = Function

class Function( MathmlMI ):
    def to_sympy( self, tail=SYMPY_NONE ):
        return PartialSympyObject( self, tail )
