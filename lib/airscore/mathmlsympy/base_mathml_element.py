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
        if isinstance( self.text, unicode ):
            u = self.text
        else:
            u = unicode( self.text, 'utf-8' )
        return DICTIONARY.get( u, u )
    
    def get_sympy_text(self):
        return self.decoded_text
    
    def pick_subclass(self):
        pass

# These imports have been moved to the end to avoid import cycles
import mathml_operators
