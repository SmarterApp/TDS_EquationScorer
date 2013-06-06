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
    