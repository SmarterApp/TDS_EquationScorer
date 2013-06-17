########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from base_mathml_element import BaseMathmlElement
from partial_sympy_object import SYMPY_NONE
from parser import mathml_element

class BaseMathmlContainer( BaseMathmlElement ):
    """The base class for all MathML container elements.
    
    The base class for all MathML elements that can contain an arbitrary list
    of other MathML elements. This includes elements like <math> and <row>, as
    well as elements listed in the `MathML <www.w3.org/math>`_ spec as containing
    an implicit <row> element.
    """
    
    validate_max_children = -1
    validate_no_text = True
    
    def get_sympy_text_list(self):
        """Return a list containing text representations of simple equations or inequalities.
        
        This method is the main loop of the parser for most MathML expressions. Most
        containers will not need to override this method, but it is worth understanding how
        it works.  One oddity worth noting is that the parser parses the expression from
        right to left, instead of the usual left-to-right.
        
        If the expression is a "chained" equation, containing
        more than one equals or inequality operator, then this function will return multiple
        strings in its return list. Each return value will be a simple equation or
        inequality--i.e., one that contains only one equals or inequality operator.
        
        If the expression is already a simple equation or inequality, then a list containing a
        single string represnting that equation or inequality will be returned.
        
        If the expression contains no equality or inequality operators, then a list containing a
        single string representing that expression will be returned.
        
        :returns: :func:`list` of :func:`str`
        """
        
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
        return super( MathmlMath, self ).get_sympy_text_list()

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

