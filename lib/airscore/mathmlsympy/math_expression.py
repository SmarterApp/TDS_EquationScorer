########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

class MathExpression( object ):
    """The representation of a MathML expression, equality, or inequality that has been returned by the parser.
    
    .. attribute:: math_node
    
        :class:`MathmlMath` The XML Element tree that was returned by the
        parser. Elements within the tree will be represented by subclasses
        of :class:`BaseMathmlElement`, which in turn subclasses
        :class:`xml.etree.ElementTree.Element`
        
    .. attribute:: sympy_response
    
        [ str ] A list of strings representing equations, inequalities or
        expressions.  This is the result of parsing the XML represented
        by :attr:`math_node`\ .  The list will consist of more than one
        element if the :attr:`math_node` contains more than one equality or inequality
        operator.  Specifically, if the MathML represented something like::
        
            A = B = C < D
        
        then the list will contain three entries, corresponding to::
        
            A = B
            B = C
            C < D
    """
    
    def __init__( self, math_node ):
        self.math_node = math_node
        self.sympy_response = math_node.get_sympy_text_list()
        
    def __str__(self):
        """Returns a string representation that can be understood by Sympy
        
        This is just a convenience wrapper for ``unicode( self ).encode('UTF-8')``
        """
        return unicode( self ).encode('UTF-8')
        
    def __unicode__(self):
        """Returns a unicode representation that can be understood by Sympy"""
        return u', '.join( self.sympy_response )
    
class MathExpressionList( list ):
    """A container for multiple :class:`MathExpression` elements.
    
    The :meth:`__str__` and :meth:`__unicode__` methods have been overridden to
    return strings that will be useful to Sympy.
    """
    
    def __str__(self):
        """Returns a string representation that can be understood by Sympy
        
        This is just a convenience wrapper for ``unicode( self ).encode('UTF-8')``
        """
        return unicode( self ).encode('UTF-8')
        
    def __unicode__(self):
        """Returns a unicode representation that can be understood by Sympy"""
        return u'[' + u', '.join( [ unicode( exp ) for exp in self ] ) + ']'