'''
Created on Jun 6, 2013

@author: temp_dmenes
'''

from parser import mathml_element, Q_MO
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import PartialSympyObject

@mathml_element('mo')
class MathmlMO( BaseMathmlElement ):
    
    is_implicit_multiplicand=False
    
    def __init__( self, tag=Q_MO, attrs={}, **kwargs ):
        """Constructor override to provide default value for tag name
        """
        super( MathmlMO, self ).__init__( tag, attrs, **kwargs )
    
    def to_sympy( self, tail ):
        return PartialSympyObject( self, tail )
    
    def pick_subclass(self):
        """This is deeply funky Python dynamic class stuff. We are reassigning an object's
        class after it was created. We do this because we didn't know which subclass to use
        until the text of the element was filled in.
        """
        if self.text in Inequality.texts:
            self.__class__ = Inequality


class Inequality( BaseMathmlElement ):
    texts = { '<':'Lt', '&lt;':'Lt', u'\u2664':'Le', '=':'Eq', '\u2665':'Ge', '&gt;':'Gt', '>':'Gt'  }

    is_inequality = True
    is_implicit_multiplicand = False
    
    def get_sympy_text(self):
        return self.texts[ self.text ]
    

PLUS_OPERATOR = MathmlMO()
PLUS_OPERATOR.text="+"
PLUS_OPERATOR.pick_subclass()

TIMES_OPERATOR = MathmlMO()
TIMES_OPERATOR.text="*"
TIMES_OPERATOR.pick_subclass()