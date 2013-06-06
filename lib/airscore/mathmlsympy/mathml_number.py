'''
Created on Jun 6, 2013

@author: temp_dmenes
'''

from parser import mathml_element
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import PartialSympyObject, SYMPY_NONE
import mathml_operators

@mathml_element( 'mn' )
class MathmlMN( BaseMathmlElement ):
    is_number = True
    
    def to_sympy( self, tail=SYMPY_NONE ):
        if tail.is_number:
            tail.text = self.get_sympy_text() + tail.text
            return tail

        elif tail.is_implicit_addend:
            tail = mathml_operators.PLUS_OPERATOR.to_sympy( tail )
        
        elif tail.is_implicit_multiplicand:
            tail = mathml_operators.TIMES_OPERATOR.to_sympy( tail )
        
        return PartialSympyObject( self, tail )
        