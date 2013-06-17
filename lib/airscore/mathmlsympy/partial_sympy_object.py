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
    
    .. attribute:: next
    
        :class:`PartialSympyObject` - The next rightward neighbor in the list.
        
    .. attribute:: is_closed
    
        :func:`bool` - Used in balancing absolute value bars.  :const:`True`
        if the parser has encountered an odd number of absolute value bars to
        the right of this point.
        
    .. attribute:: is_implicit_mutliplicand
    
        :func:`bool` - The `is_implicit_multiplicand` attribute of the
        :class:`airscore.mathmlsympy.base_mathml_element.BaseMathmlElement`
        that generated this object.
        
    .. attribute:: is_implicit_addend
    
        :func:`bool` - The `is_implicit_addend` attribute of the
        :class:`airscore.mathmlsympy.base_mathml_element.BaseMathmlElement`
        that generated this object.
        
    .. attribute:: is_number
    
        :func:`bool` - The `is_number` attribute of the
        :class:`airscore.mathmlsympy.base_mathml_element.BaseMathmlElement`
        that generated this object.
        
    .. attribute:: text
    
        :func:`unicode` - The result of the :meth:`BaseMathmlElement.get_sympy_text`
        method of the :class:`airscore.mathmlsympy.base_mathml_element.BaseMathmlElement`
        object that generated this object.
    '''
    def __init__( self, el, tail ):
        self.next = tail
        self.is_closed = tail.is_closed if tail is not None else False
        
        self.is_implicit_multiplicand = el.is_implicit_multiplicand if el is not None else False
        self.is_implicit_addend = el.is_implicit_addend if el is not None else False
        self.is_number = el.is_number if el is not None else False
        self.text = el.get_sympy_text() if el is not None else ''
        
    def itertext(self):
        """Iterate through the linked list, returning the :attr:`text` attribute
        of each node.
        
        :returns: :class:`iterator` of :class:`unicode`
        """
        x = self
        while x is not SYMPY_NONE:
            yield x.text
            x = x.next
            
    def get_sympy_text(self):
        """The concatenated :attr:`text` attributes of this node and all of the
        nodes to its right.
        
        :returns: :class:`unicode`
        """
        return ''.join( self.itertext() )
        
SYMPY_NONE = PartialSympyObject( None, None )
