###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

class MathExpression( object ):
    
    def __init__( self, math_node ):
        self.math_node = math_node
        self.sympy_response = math_node.get_sympy_text_list()
        
    def __str__(self):
        return unicode( self ).encode('UTF-8')
        
    def __unicode__(self):
        return u', '.join( self.sympy_response )
    
class MathExpressionList( list ):

    def __str__(self):
        return unicode( self ).encode('UTF-8')
        
    def __unicode__(self):
        return u'[' + u', '.join( [ unicode( exp ) for exp in self ] ) + ']'