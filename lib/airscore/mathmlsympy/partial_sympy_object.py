########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

import logging

LOGGER = logging.getLogger( 'airscore.mathmlsympy.partial_sympy_object' )

class PartialSympyObject( object ):
    '''An element in a linked list that represents a Sympy expression
    
    :param el: The mathml element from which this object is derived
    
    :type el: :class:`BaseMathmlElement`
    
    :param tail: The next item in the list
    
    :type tail: :class:`PartialSympyObject`
    '''
    def __init__( self, el, tail ):
        self.next = tail
        self.is_closed = tail.is_closed if tail is not None else False
        
        self.is_implicit_multiplicand = el.is_implicit_multiplicand if el is not None else False
        self.is_implicit_addend = el.is_implicit_addend if el is not None else False
        self.is_number = el.is_number if el is not None else False
        self.text = el.get_sympy_text() if el is not None else ''
        
    def itertext(self):
        x = self
        while x is not SYMPY_NONE:
            yield x.text
            x = x.next
            
    def get_sympy_text(self):
        return ''.join( self.itertext() )
        
SYMPY_NONE = PartialSympyObject( None, None )
