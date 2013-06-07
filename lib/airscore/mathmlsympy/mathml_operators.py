###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from parser import mathml_element, Q_MO
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import PartialSympyObject, SYMPY_NONE
import mathml_number

@mathml_element('mo')
class MathmlMO( BaseMathmlElement ):
    
    is_implicit_multiplicand=False
    
    def __init__( self, tag=Q_MO, attrs={}, **kwargs ):
        """Constructor override to provide default value for tag name
        """
        super( MathmlMO, self ).__init__( tag, attrs, **kwargs )
    
    def to_sympy( self, tail=SYMPY_NONE ):
        return PartialSympyObject( self, tail )
    
    def pick_subclass(self):
        """This is deeply funky Python dynamic class stuff. We are reassigning an object's
        class after it was created. We do this because we didn't know which subclass to use
        until the text of the element was filled in.
        """
        if self.decoded_text in Inequality.texts:
            self.__class__ = Inequality
        elif self.decoded_text == '.':
            self.__class__ = mathml_number.MathmlMN


class Inequality( BaseMathmlElement ):
    texts = { '<':'Lt', '&lt;':'Lt', u'\u2664':'Le', '=':'Eq', '\u2665':'Ge', '&gt;':'Gt', '>':'Gt'  }

    is_inequality = True
    is_implicit_multiplicand = False
    
    def get_sympy_text(self):
        return self.texts[ self.decoded_text ]
    

PLUS_OPERATOR = MathmlMO()
PLUS_OPERATOR.text="+"
PLUS_OPERATOR.pick_subclass()

TIMES_OPERATOR = MathmlMO()
TIMES_OPERATOR.text="*"
TIMES_OPERATOR.pick_subclass()
