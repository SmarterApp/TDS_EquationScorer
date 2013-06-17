#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

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
        txt = self.decoded_text
        for cls in ( Inequality, Pipe, GroupClose, GroupOpen, DecimalPoint ):
            if txt in cls.symbols:
                self.__class__ = cls
                break


class Inequality( MathmlMO ):
    
    symbols = { u'<':u'Lt', u'&lt;':u'Lt', u'\u2264':u'Le', u'=':u'Eq', u'\u2265':u'Ge', u'&gt;':u'Gt', u'>':u'Gt'  }
    is_inequality = True
    
    def get_sympy_text(self):
        return self.symbols[ self.decoded_text ]

class GroupClose( MathmlMO ):
    
    symbols = (u')',)
    
    def to_sympy( self, tail=SYMPY_NONE ):
        # Revert to the "expression" logic that is on the BaseMathmlExpression class
        # This is the behavior that tries to do implicit multiplication by whatever follows
        return super( MathmlMO, self ).to_sympy( tail )
    
class GroupOpen( MathmlMO ):
    
    symbols = (u'(',)
    is_implicit_multiplicand = True
    
class Pipe( MathmlMO ):
    
    symbols = (u'|',)
    
    @property
    def is_implicit_multiplicand(self):
        return self.is_opening

    def get_sympy_text( self ):
        if self.is_opening:
            return u'Abs('
        else:
            return u')'
    
    def to_sympy( self, tail=SYMPY_NONE ):
        self.is_opening = tail.is_closed
        if self.is_opening:
            tail = super( Pipe, self ).to_sympy( tail )
            tail.is_closed = False
        else:
            tail = super( MathmlMO, self ).to_sympy( tail )
            tail.is_closed = True
        return tail
    
# The DecimalPoint class inherits from a mathml number even though it is represented by
# a mathml operator in the XML. 
class DecimalPoint( mathml_number.MathmlMN ):
    
    symbols = u'.'

PLUS_OPERATOR = MathmlMO()
PLUS_OPERATOR.text = u"+"
PLUS_OPERATOR.pick_subclass()

TIMES_OPERATOR = MathmlMO()
TIMES_OPERATOR.text = u"*"
TIMES_OPERATOR.pick_subclass()
