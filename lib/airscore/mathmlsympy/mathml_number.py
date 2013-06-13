########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from parser import mathml_element
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import PartialSympyObject, SYMPY_NONE
import mathml_operators

@mathml_element( 'mn' )
class MathmlMN( BaseMathmlElement ):
    is_number = True
    
    @property
    def is_non_neg_integer(self):
        return self.decoded_text.isdigit()
    
    def to_sympy( self, tail=SYMPY_NONE ):
        if tail.is_number:
            tail.text = self.get_sympy_text() + tail.text
            return tail

        elif tail.is_implicit_addend:
            tail = mathml_operators.PLUS_OPERATOR.to_sympy( tail )
        
        elif tail.is_implicit_multiplicand:
            tail = mathml_operators.TIMES_OPERATOR.to_sympy( tail )
        
        return PartialSympyObject( self, tail )
        