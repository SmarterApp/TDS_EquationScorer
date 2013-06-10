###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

import logging

from xml.etree import ElementTree as et
# Note: in-module imports are moved to end to fix cycles

MATHML_NAMESPACE = u'http://www.w3.org/1998/Math/MathML'
_ELEMENT_CLASSES = {}

LOGGER = logging.getLogger('airscore.mathmlsympy.parser')

def q( s, namespace=MATHML_NAMESPACE ):
    return u'{{{}}}{}'.format( namespace, s )

Q_MATH = q(u'math')
Q_RESPONSE = u'response'
Q_MSTYLE = q(u'mstyle')
Q_MO = q(u'mo')

def mathml_element( *args ):
    """A decorator which registers the decorated class as a mathml element class
    """
    if len( args ) == 1 and isinstance( args[0], type ):
        name = q( args[0].__name__ )
        _ELEMENT_CLASSES[ name ] = args[0]
        return args[0]
    elif len( args ) == 1 and isinstance( args[0], ( str, unicode ) ):
        def deco( cls ):
            name = q( args[0] )
            _ELEMENT_CLASSES[ name ] = cls
            return cls
        return deco
    else:
        def deco( cls ):
            for name in args:
                qname = q( name )
                _ELEMENT_CLASSES[ qname ] = cls
            return cls
        return deco


class MathmlBuilder( et.TreeBuilder ):
    
    def __init__(self):
        super( MathmlBuilder, self ).__init__( self.mathml_element_factory )
        
    @staticmethod
    def mathml_element_factory( tag, attrs={}, **kwargs ):
        """An XML element factory that returns special classes for MATHML elements
        """
        cls = _ELEMENT_CLASSES.get( tag, et.Element )
        return cls( tag, attrs, **kwargs )
    
    def end( self, tag ):
        """We are doing funky stuff with dynamic classes in the end tag processing
        
        Specifically, we are giving the newly-created element a chance to assign a new value to its
        __class__ property, effectivley changing its class. We are permitting this because we don't
        have enough information when processing the start tag to fully determine the class.
        """
        el = super( MathmlBuilder, self ).end( tag )
        if isinstance( el, BaseMathmlElement ):
            el.pick_subclass()
            el.validate()



def process_mathml_data( mathml_string, encoding=None ):
    if isinstance( mathml_string, unicode ):
        if encoding is None:
            encoding = 'UTF-8'
        mathml_string = mathml_string.encode( encoding )
    parser = et.XMLParser( target = MathmlBuilder(), encoding=encoding )
    root_node = et.fromstring( mathml_string, parser )
    if root_node.tag == Q_MATH:
        math_nodes = [ root_node ]
    elif root_node.tag == Q_RESPONSE:
        math_nodes = root_node.findall( u'./*' )
    else:
        raise ValueError( 'XML root_node must have either a <mathml:math> element or a <response> element as its root ' )
    
    expressions = MathExpressionList()
    for math_node in math_nodes:
        if math_node.tag != Q_MATH:
            raise ValueError( "MathML2SymPyString should be called with a top level node with name 'math', this node has name {}" \
                                    .format( math_node.tag )  )
        expressions.append( MathExpression( math_node ) )
    return expressions

# These imports are at the end to fix cycles
from base_mathml_element import BaseMathmlElement
from math_expression import MathExpression, MathExpressionList
