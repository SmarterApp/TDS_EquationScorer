#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from base_mathml_element import BaseMathmlElement
from parser import mathml_element

@mathml_element( 'mroot' )
class MathmlMRoot( BaseMathmlElement ):
    
    validate_max_children = 2
    validate_min_children = 2
    validate_no_text = True
    
    def get_sympy_text( self ):
        return u'('+ self[0].get_sympy_text() + u')**(1/(' + self[1].get_sympy_text() + u'))'

@mathml_element( 'msup' )
class MathmlMSup( BaseMathmlElement ):
    
    validate_max_children = 2
    validate_min_children = 2
    validate_no_text = True
    
    def get_sympy_text( self ):
        return u'(' + self[0].get_sympy_text() + u')**(' + self[1].get_sympy_text() + u')'

@mathml_element( 'msub' )
class MathmlMSub( BaseMathmlElement ):
    
    validate_max_children = 2
    validate_min_children = 2
    validate_no_text = True
    
    def get_sympy_text( self ):
        return self[0].get_sympy_text() + u'_' + self[1].get_sympy_text()

@mathml_element( 'msubsup' )
class MathmlMSubSup( BaseMathmlElement ):
    
    validate_max_children = 3
    validate_min_children = 3
    validate_no_text = True
    
    def get_sympy_text( self ):
        return u'(' + self[0].get_sympy_text() + u'_' + self[1].get_sympy_text() + u')**(' + self[2].get_sympy_text() + u')'
