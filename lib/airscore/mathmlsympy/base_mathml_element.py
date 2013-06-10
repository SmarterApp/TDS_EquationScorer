###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from xml.etree import ElementTree as et

from partial_sympy_object import PartialSympyObject, SYMPY_NONE
from substitutions import DICTIONARY
# some in-module imports moved to end to avoid cycles

class BaseMathmlElement( et.Element ):

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
        
        :param tail: The head of a linked list of sympy objects which will become
            the tail of the newly created object

        :type tail: :class:`PartialSympyObject`
        
        :returns: :class:`PartialSympyObject`
        """
        if tail.is_implicit_multiplicand:
            tail = mathml_operators.TIMES_OPERATOR.to_sympy( tail )
        return PartialSympyObject( self, tail )
    
    @property
    def decoded_text(self):
        """Return the text content of self as unicode.
        """
        if self.text is None:
            return None
        if isinstance( self.text, unicode ):
            u = self.text
        else:
            u = unicode( self.text, 'utf-8' )
        return DICTIONARY.get( u, u )
    
    def get_sympy_text(self):
        return self.decoded_text
    
    def pick_subclass(self):
        pass
    
    def validate(self):
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
