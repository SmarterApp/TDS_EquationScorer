###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from base_mathml_element import BaseMathmlElement
from parser import mathml_element

@mathml_element( 'mroot' )
class MathmlMRoot( BaseMathmlElement ):
    
    def get_sympy_text( self ):
        return '('+ self[0].get_sympy_text() + ')**(1/(' + self[1].get_sympy_text() + '))'

@mathml_element( 'msup' )
class MathmlMSup( BaseMathmlElement ):
    
    def get_sympy_text( self ):
        return '('+ self[0].get_sympy_text() + ')**(' + self[1].get_sympy_text() + ')'

@mathml_element( 'msub' )
class MathmlMSub( BaseMathmlElement ):
    
    def get_sympy_text( self ):
        return self[0].get_sympy_text() + '_' + self[1].get_sympy_text()

@mathml_element( 'msubsup' )
class MathmlMSubSup( BaseMathmlElement ):
    
    def get_sympy_text( self ):
        return '(' + self[0].get_sympy_text() + '_' + self[1].get_sympy_text() + ')**(' + self[2].get_sympy_text() + ')'

