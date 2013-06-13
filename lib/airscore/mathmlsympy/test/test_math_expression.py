########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from xml.etree import ElementTree as et

from airscore.mathmlsympy.math_expression import MathExpression, MathExpressionList
import abstract_parser_test

class TestMathExpressions( abstract_parser_test.TestCase ):
    
    def test_math_expression_to_str(self):
        node = et.fromstring( abstract_parser_test.XML_1, self.parser )
        archetype = 'Le(1*x,3)'
        mexp = MathExpression( node )
        self.assertEquals( str( mexp ), archetype, "Got {!r} instead of {!r}".format( str( mexp ), archetype ) )
        
    def test_math_expression_list_to_str(self):
        node = et.fromstring( abstract_parser_test.XML_1, self.parser )
        archetype = '[Le(1*x,3), Le(1*x,3)]'
        mexp = MathExpression( node )
        mexp_list = MathExpressionList( ( mexp, mexp ) )
        self.assertEquals( str( mexp_list ), archetype, "Got {!r} instead of {!r}".format( str( mexp_list ), archetype ) )
        
