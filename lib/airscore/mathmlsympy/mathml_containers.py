'''
Created on Jun 6, 2013

@author: temp_dmenes
'''
from base_mathml_element import BaseMathmlElement
from partial_sympy_object import SYMPY_NONE
from parser import mathml_element

class BaseMathmlContainer( BaseMathmlElement ):
    
    def get_sympy_text_list(self):
        
        # Split the expression on equality or inequality symbols
        tail = SYMPY_NONE
        inequalities = [] 
        expressions = [SYMPY_NONE]
        i = 0
        for child in self[::-1]:
            if child.is_inequality:
                inequalities.append( child )
                expressions[i] = tail
                expressions.append( SYMPY_NONE )
                tail = SYMPY_NONE
                i += 1
            else:
                tail = child.to_sympy( tail )
        expressions[i] = tail
        
        # Add a string for each equality or inequality expression
        ret = []
        for i in range( len( inequalities ) ):
            ret.append( '{}({},{})'.format( inequalities[i].get_sympy_text(),
                    expressions[i+1].get_sympy_text(),
                    expressions[i].get_sympy_text() ) )
        return ret

    def get_sympy_text(self):
        lst = self.get_sympy_text_list()
        s = ','.join( lst )
        if len( lst ) > 1:
            return '[' + s + ']'
        else:
            return s
        
@mathml_element( 'math' )
class MathmlMath( BaseMathmlContainer ):
    def get_sympy_text_list(self):
        if len( self ) == 1 and isinstance( self[0], MathmlMStyle ):
            return self[0].get_sympy_text_list()
        return super( self, MathmlMath ).get_sympy_text_list()

@mathml_element( 'mstyle' )
class MathmlMStyle( BaseMathmlContainer ):
    pass

@mathml_element( 'mrow' )
class MathmlMRow( BaseMathmlContainer ):
    pass
