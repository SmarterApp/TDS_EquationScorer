#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from xml.etree import ElementTree as et

from partial_sympy_object import PartialSympyObject, SYMPY_NONE
from substitutions import DICTIONARY
# some in-module imports moved to end to avoid cycles

class BaseMathmlElement( et.Element ):
    """This is the base class for all MathML elements in the XML tree
    
    .. attribute:: is_implicit_addend
    
       :func:`bool` - This node may appear as the implicit addend of an
       integer (as the fractional part of a mixed number).
       
    .. attribute:: is_implicit_multiplicand
    
       :func:`bool` - When a number or a symbol appears to the left of this
       node, an implicit multiplication should be performed.
       
    .. attribute:: is_inequality
    
       :func:`bool` - This is an equal sign or inequality operator. A chained
       equation can be broken on this node.
       
    .. attribute:: is_number
    
       :func:`bool` - This node contains a number (digits, decimal
       points, etc).
       
    .. attribute:: is_non_neg_integer
    
       :func:`bool` - This node is a non-negative integer. This flag is used
       to detect when the numerator and denominator of a fraction contain simple
       numbers, allowing us to use the fraction as part of a mixed number (see
       :attr:`is_implicit_addend`).
       
    .. attribute:: validate_max_children
    
       :func:`int` - Maximum number of children permitted for this node.

    .. attribute:: validate_min_children
    
       :func:`int` - Minimum number of children permitted for this node.
       
    .. attribute:: validate_no_text
    
       :func:`bool` - If :const:`True`, it is an error for this node to
       contain text directly.  Text may still exist inside of nested nodes.
       
    .. attribute:: validate_required_attributes
    
      :class:`set` of :func:`str` - A set containing the names of required
      attributes. Not namespace aware.
    """

    is_implicit_addend = False
    is_implicit_multiplicand = True
    is_inequality = False
    is_number = False
    is_non_neg_integer = False
    
    validate_max_children = 0
    validate_min_children = 0
    validate_no_text = False
    validate_required_attributes=set()
    
    def to_sympy( self, tail=SYMPY_NONE ):
        """Return oneself as a "partial sympy object"
        
        You will need to override this routine if you are changing the way this
        node combines with its neighbor nodes.  The default implementation
        concatenates this node with its right-hand neighbor, adding a mutliplcation
        operator to the list first if the right-hand neighbor is a suitable implicit
        multiplicand.
        
        Override :meth:`get_sympy_text` instead if you need to change how this node
        and its children are represented in the output, but not how this node is
        related to its siblings.
        
        :param tail: The head of a linked list of sympy objects which will become
            the tail of the newly created object

        :type tail: :class:`airscore.mathmlsympy.partial_sympy_object.PartialSympyObject`
        
        :returns: :class:`airscore.mathmlsympy.partial_sympy_object.PartialSympyObject`
        """
        if tail.is_implicit_multiplicand:
            tail = mathml_operators.TIMES_OPERATOR.to_sympy( tail )
        return PartialSympyObject( self, tail )
    
    @property
    def decoded_text(self):
        """:class:`unicode` The text content
        
        The default implementation decodes a limited dictionary of common unicode
        values to sympy equivalents.
        """
        if self.text is None:
            return None
        if isinstance( self.text, unicode ):
            u = self.text
        else:
            u = unicode( self.text, 'utf-8' )
        return DICTIONARY.get( u, u )
    
    def get_sympy_text(self):
        """Get a string representing this node, including children
        
        This is the main method that you will need to override in order
        to control how this node and its children are rendered in the sympy
        output.
        
        The default implementation simply returns the :attr:`decode_text`
        attribute.
        
        Override :meth:`to_sympy` instead if you need to control how this node
        relates to its neighbors.  
        
        :returns: :class:`unicode` - The string representing this node in a
            sympy expression
        """
        return self.decoded_text
    
    def pick_subclass(self):
        """Change the leopard's spots to zebra stripes
        
        The :mod:`xml.etree.ElementTree` parsing mechanism forces us to choose
        the class for new elements when the start tag has been parsed, but before
        any of the content has been read.  There are a few MathML constructs
        for which we need different classes, but they are represented
        by the same start tag.  Our parser calls this method after the end
        tag has been processed, in order to give the element a chance to make
        any changes it needs to make to finalize its class selection.
        
        In most cases, this method does nothing (the default behavior). In a few
        cases, however, this method will assign a new value to the instance's
        :attr:`__class__` property in order to change the object into an
        instance of a subclass of its original class.
        
        We are using an admittedly obscure Python "feature," and I can't recommend
        that you make a habit of altering the classes of existing objects. But for
        this limited purpose it seemed the cleanest solution.
        
        :returns: :const:`None`
        """
        pass
    
    def validate(self):
        """Validate the node content
        
        This method is called during the processing of the XML end tag, immediately
        after the call to :meth:`pick_subclass`. Subclasses should perform any
        required validation of the newly-created MathML object.  An error should
        be raised for a validation failure (usually :class:`ValueError`)
        
        The default implementation performs the following steps:
        
         - Validate the number of children against the :attr:`validate_min_children`
           and :attr:`validate_max_children` properties
           
         - If :attr:`validate_no_text` is :const:`True`, confirm that the element contains
           no text.
           
         - Confirm that children (if any) are subclasses of :class:`BaseMathmlElement`
         
         - Confirm that any attributes listed in :attr:`validate_required_attributes`
           are present (but perform no validation on the attribute values)
           
        :returns: :const:`None`
        
        :raises: :exc:`ValueError`
        """
        if ( self.validate_min_children == self.validate_max_children ) \
                and len( self ) != self.validate_min_children:
            raise ValueError( "Element {tag} must have exactly {n} children, found {m}".format(
                    tag=self.tag, n=self.validate_min_children, m=len( self ) ) )
            
        if self.validate_max_children >= 0 and self.validate_max_children < len( self ):
            raise ValueError( "Element {tag} may have no more than {n} children, found {m}".format(
                    tag=self.tag, n=self.validate_max_children, m=len( self ) ) )
            
        if self.validate_min_children > len( self ):
            raise ValueError( "Element {tag} must have at least {n} children, found {m}".format(
                    tag=self.tag, n=self.validate_min_children, m=len( self ) ) )
            
        if self.validate_no_text and self.text is not None and self.text.strip():
            raise ValueError( "Element {tag} may not have text content".format( self.tag ) )
        
        for child in self:
            if not isinstance( child, BaseMathmlElement ):
                raise ValueError( "I do not know how to handle the tag {}".format( child.tag ) )
            if self.validate_no_text and child.tail is not None and child.tail.strip():
                raise ValueError( "Element {tag} may not have text content".format( self.tag ) )
            child.validate()
        
        for key in self.validate_required_attributes:
            if key not in self.attrib:
                raise ValueError( "Element {tag} missing required attribute {}".format( self.tag, key ) )
            
# These imports have been moved to the end to avoid import cycles
import mathml_operators
