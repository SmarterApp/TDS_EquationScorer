########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from base_mathml_element import BaseMathmlElement
from parser import mathml_element

@mathml_element( 'mfrac' )
class MathmlMFrac( BaseMathmlElement ):
    
    validate_max_children = 2
    validate_min_children = 2
    validate_no_text = True
    
    def get_sympy_text( self ):
        return u'/'.join( [ child.get_sympy_text() for child in self ] )

    @property
    def is_implicit_addend( self ):
        return self[0].is_non_neg_integer and self[1].is_non_neg_integer
