###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from base_mathml_element import BaseMathmlElement
from partial_sympy_object import SYMPY_NONE
from parser import mathml_element

class BaseMathmlContainer( BaseMathmlElement ):
    
    validate_max_children = -1
    validate_no_text = True
    
    def get_sympy_text_list(self):
        
        # Split the expression on equality or inequality symbols
        tail = SYMPY_NONE
        inequalities = [] 
        expressions = [SYMPY_NONE]
        i = 0
        for child in self[::-1]:
            if child.is_inequality:
                inequalities.append( child )
                expressions[i] = tail
                expressions.append( SYMPY_NONE )
                tail = SYMPY_NONE
                i += 1
            else:
                tail = child.to_sympy( tail )
        expressions[i] = tail
        
        # Add a string for each equality or inequality expression
        ret = []
        if len( inequalities ) == 0:
            ret.append( expressions[0].get_sympy_text() )
        while i > 0:
            i -= 1
            ret.append( u'{}({},{})'.format( inequalities[i].get_sympy_text(),
                    expressions[i+1].get_sympy_text(),
                    expressions[i].get_sympy_text() ) )
        return ret

    def get_sympy_text(self):
        lst = self.get_sympy_text_list()
        s = ','.join( lst )
        if len( lst ) > 1:
            return u'[' + s + u']'
        else:
            return s
        
@mathml_element( 'math' )
class MathmlMath( BaseMathmlContainer ):
    def get_sympy_text_list(self):
        if len( self ) == 1 and isinstance( self[0], MathmlMStyle ):
            return self[0].get_sympy_text_list()
        return super( self, MathmlMath ).get_sympy_text_list()

@mathml_element( 'mstyle' )
class MathmlMStyle( BaseMathmlContainer ):
    pass

@mathml_element( 'mrow' )
class MathmlMRow( BaseMathmlContainer ):
    def get_sympy_text( self ):
        return u'(' + super( MathmlMRow, self ).get_sympy_text() + u')'

    @property
    def is_non_neg_integer(self):
        return all( [ child.is_non_neg_integer for child in self ])
    
@mathml_element( 'mfenced' )
class MathmlMFenced( BaseMathmlContainer ):
    def get_sympy_text( self ):
        return self.get( 'open', u'(' ) \
            + super( MathmlMFenced, self ).get_sympy_text() \
            + self.get( 'close', u')' )

@mathml_element( 'msqrt' )
class MathmlMSqrt( BaseMathmlContainer ):
    def get_sympy_text( self ):
        return u'sqrt(' + super( MathmlMSqrt, self ).get_sympy_text() + u')'

