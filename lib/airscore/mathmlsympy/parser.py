########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

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
    
    This decorator registers the association between a class and an element name
    for the :class:`MathMLBuilder`. In order to have the :class:`MathMLBuilder`
    use a particular class instead of the default :class:`xml.etree.ElementTree.Element`
    class to represent a given XML element, decorate your class definition with this
    decorator.
    
    There are three permitted calling conventions.  You can use the decorator
    without arguments, like so::
        
        @mathml_element
        class bob( BaseMathmlElement ):
            ...
     
    in which case the new class will be used for elements named :samp:`<bob>` in the MathML
    namespace.  This usage is not ideal, as it requires your Python class to have the
    same name (including case) as the MathML element.
    
    You avoid this problem by specifying an element name like this::
    
        @mathml_element( 'bob' )
        class MathMLBob( BaseMathmlElement ):
            ...
            
    Finally, if you have a class that should be associated with multiple MathML tag names,
    you can specify all of the names as arguments to the :func:`mathml_element decorator`\ ::
    
        @mathml_element( 'bob', 'jim', 'joe' )
        class MathMLBob( BaseMathmlElement ):
            ...
            
    In every case, the classes will only be used for elements in the MathML namespace
    (`http://www.w3.org/1998/Math/MathML`)
    
    No special effort beyond the use of this decorator is required to register
    new classes for handling MathML elements. However, you must be certain that
    the modules containing your classes have been imported before attempting to
    process the XML data.
    """
    if len( args ) == 1 and isinstance( args[0], type ):
        name = q( args[0].__name__ )
        _ELEMENT_CLASSES[ name ] = args[0]
        return args[0]
    else:
        def deco( cls ):
            for name in args:
                qname = q( name )
                _ELEMENT_CLASSES[ qname ] = cls
            return cls
        return deco


class MathmlBuilder( et.TreeBuilder ):
    """Tree Builder to create MathML-aware objects
    
    This class inherits from the :class:`xml.etree.ElementTree.TreeBuilder` in
    the standard Python libraries. It is used when parsing an XML tree that
    contains MathML expressions. By using this builder instead of the default
    builder, we create a tree that contains our custom MathML objects, rather
    than the default :class:`xml.etree.ElementTree.Element` objects.
    """
    
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
    """Convert MathML into a form that can be understood by Sympy
    
    The provided string must either contain a :samp:`<mathml:math>` element as the root, or
    it must contain a :samp:`<response>` element (no namespace), which contains zero or
    more :samp:`<mathml:math>` elements as children.
    
    :param mathml_string: A string containing a :samp:`<mathml:math>` or :samp:`<response>` element
    
    :type mathml_string: :func:`str` or :func:`unicode`. If the provided object is :func:`unicode`,
        it will be converted to a string by the specified encoding.
    
    :param encoding: Name of the encoding that will be used in parsing the mathml_string. Defaults to UTF-8
    
    :type encoding: str
    
    :returns: A :class:`MathExpressionList` object equivalent to the MathML original. This object's
        :meth:`__unicode__` method returns a string that can be passed to Sympy
        
    """
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
        raise ValueError( 'XML root_node must have either a :samp:`<mathml:math>` element or a :samp:`<response>` element as its root ' )
    
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
