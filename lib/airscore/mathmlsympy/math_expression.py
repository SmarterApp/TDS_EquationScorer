'''
Created on Jun 6, 2013

@author: temp_dmenes
'''
class MathExpression( object ):
    
    def __init__( self, math_node ):
        self.math_node = math_node
        self.sympy_response = math_node.get_sympy_text_list()
    