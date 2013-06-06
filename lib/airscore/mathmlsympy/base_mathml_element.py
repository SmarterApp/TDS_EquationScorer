'''
Created on Jun 5, 2013

@author: temp_dmenes
'''

from xml.etree import ElementTree as et

from partial_sympy_object import PartialSympyObject, SYMPY_NONE
# some in-module imports moved to end to avoid cycles

class BaseMathmlElement( et.Element ):

    is_implicit_addend = False
    is_implicit_multiplicand = True
    is_inequality = False
    is_number = False
    
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
        
    def get_sympy_text(self):
        return self.text
    
    def pick_subclass(self):
        pass

# These imports have been moved to the end to avoid import cycles
import mathml_operators
