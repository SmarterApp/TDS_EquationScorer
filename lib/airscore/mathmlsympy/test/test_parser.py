'''
Created on Jun 6, 2013

@author: temp_dmenes
'''
import unittest
from xml.etree import ElementTree as et
import logging

from airscore.mathmlsympy.parser import MathmlBuilder, process_mathml_data
from airscore.mathmlsympy.mathml_containers import MathmlMath, MathmlMStyle
from airscore.mathmlsympy.mathml_number import MathmlMN
from airscore.mathmlsympy.mathml_identifier import MathmlMI
from airscore.mathmlsympy.mathml_operators import MathmlMO, Inequality

XML_1 = u"""
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
 <mstyle displaystyle="true">
  <mn>1</mn><mi>x</mi><mo>\u2664</mo><mn>3</mn>
 </mstyle>
</math>
""".encode('utf-8')

LOGGER=logging.getLogger()

class TestBuilder( unittest.TestCase ):
    
    @property
    def parser(self):
        return et.XMLParser( target = MathmlBuilder(), encoding="utf-8" )
        
    def test_build_tree(self):
        tree = et.fromstring( XML_1, self.parser )
        self.assertIsInstance( tree, MathmlMath, "Didn't get correct type for <math> element: " )
        self.assertIsInstance( tree[0], MathmlMStyle, "Didn't get correct type for <mstyle> element: " )
        self.assertIsInstance( tree[0][0], MathmlMN, "Didn't get correct type for <mn> element: " )
        self.assertIsInstance( tree[0][1], MathmlMI, "Didn't get correct type for <mi> element: " )
        self.assertIsInstance( tree[0][2], Inequality, "Didn't get correct type for <mo>=</mo> element: " )
        self.assertIsInstance( tree[0][3], MathmlMN, "Didn't get correct type for <mn> element: " )
        
    def test_number_1(self):
        '''Basic construction and properties of a number
        '''
        node = et.fromstring( '<mn xmlns="http://www.w3.org/1998/Math/MathML">123</mn>', self.parser )
        self.assertIsInstance( node, MathmlMN, "Didn't get correct type for <mn> element: " )
        self.assertEquals( node.get_sympy_text(), '123', "Got the wrong content in the XML node" )
        self.assertTrue( node.is_number, "Number says it isn't a number" )
        self.assertTrue( node.is_implicit_multiplicand, "Number says it cannot be implicitly mutliplied" )
        self.assertFalse( node.is_implicit_addend, "Number says it can be implicitly added" )
        self.assertFalse( node.is_inequality, "Number says it is an equality or inequality operator" )
        sympy = node.to_sympy()
        self.assertEquals( sympy.get_sympy_text(), '123', "Got the wrong content from the sympy linked list" )
        
    def test_number_2(self):
        '''Number munging
        '''
        node_r = et.fromstring( '<mn xmlns="http://www.w3.org/1998/Math/MathML">456</mn>', self.parser )
        node_l = et.fromstring( '<mn xmlns="http://www.w3.org/1998/Math/MathML">123</mn>', self.parser )
        sympy = node_r.to_sympy()
        sympy = node_l.to_sympy( sympy )
        self.assertEquals( sympy.get_sympy_text(), '123456', "Got the wrong content from the sympy linked list" )
        
    def test_identifier_1(self):
        '''Basic construction and properties of an identifier
        '''
        node = et.fromstring( '<mi xmlns="http://www.w3.org/1998/Math/MathML">bob</mi>', self.parser )
        self.assertIsInstance( node, MathmlMI, "Didn't get correct type for <mi> element: " )
        self.assertEquals( node.get_sympy_text(), 'bob', "Got the wrong content in the XML node" )
        self.assertFalse( node.is_number, "Identifier says it is a number" )
        self.assertTrue( node.is_implicit_multiplicand, "Identifier says it cannot be implicitly mutliplied" )
        self.assertFalse( node.is_implicit_addend, "Identifier says it can be implicitly added" )
        self.assertFalse( node.is_inequality, "Identifier says it is an equality or inequality operator" )
        sympy = node.to_sympy()
        self.assertEquals( sympy.get_sympy_text(), 'bob', "Got the wrong content from the sympy linked list" )
        
    def test_identifier_2(self):
        '''Test implicit multiplication between two identifiers
        '''
        node_r = et.fromstring( '<mi xmlns="http://www.w3.org/1998/Math/MathML">x</mi>', self.parser )
        node_l = et.fromstring( '<mi xmlns="http://www.w3.org/1998/Math/MathML">y</mi>', self.parser )
        sympy = node_r.to_sympy()
        sympy = node_l.to_sympy( sympy )
        self.assertEquals( sympy.get_sympy_text(), 'y*x', "Got the wrong content from the sympy linked list" )
        
    def test_number_identifier_1(self):
        '''Test implicit multiplication of an identifier by a number
        '''
        node_r = et.fromstring( '<mi xmlns="http://www.w3.org/1998/Math/MathML">x</mi>', self.parser )
        node_l = et.fromstring( '<mn xmlns="http://www.w3.org/1998/Math/MathML">62</mn>', self.parser )
        sympy = node_r.to_sympy()
        sympy = node_l.to_sympy( sympy )
        self.assertEquals( sympy.get_sympy_text(), '62*x', "Got the wrong content from the sympy linked list" )
        
    def test_number_identifier_2(self):
        '''Test implicit multiplication of a number by an identifier
        '''
        node_r = et.fromstring( '<mn xmlns="http://www.w3.org/1998/Math/MathML">62</mn>', self.parser )
        node_l = et.fromstring( '<mi xmlns="http://www.w3.org/1998/Math/MathML">x</mi>', self.parser )
        sympy = node_r.to_sympy()
        sympy = node_l.to_sympy( sympy )
        self.assertEquals( sympy.get_sympy_text(), 'x*62', "Got the wrong content from the sympy linked list" )
        
    def test_inequality_operators_1(self):
        operators = { '&lt;':'Lt', u'\u2664':'Le', '=':'Eq', '\u2665':'Ge', '&gt;':'Gt', '>':'Gt'  }
    
        for operator in operators:
            operator = operator.encode('utf-8')
            node = et.fromstring( '<mo xmlns="http://www.w3.org/1998/Math/MathML">{}</mo>'.format( operator ),
                                    self.parser )
            self.assertIsInstance( node, Inequality, "Didn't get correct type for <mo>{}</mo> element".format( operator ) )
            self.assertEquals( node.get_sympy_text(), operators[ unicode( operator, 'utf-8' ) ], "Got the wrong content in the XML node" )
            self.assertFalse( node.is_number, "Operator says it is a number" )
            self.assertFalse( node.is_implicit_multiplicand, "Operator says it can be implicitly mutliplied" )
            self.assertFalse( node.is_implicit_addend, "Operator says it can be implicitly added" )
            self.assertTrue( node.is_inequality, "Inequality says it is not an equality or inequality operator" )
            
    def test_operators_2(self):
        node = et.fromstring( '<mo xmlns="http://www.w3.org/1998/Math/MathML">+</mo>',
                                self.parser )
        self.assertFalse( isinstance( node, Inequality ), "Thinks <mo>+</mo> element os an inequality" )
        self.assertIsInstance( node, MathmlMO, "Didn't get correct type for <mo>+</mo> element" )
        self.assertEquals( node.get_sympy_text(), '+', "Got the wrong content in the XML node" )
        self.assertFalse( node.is_number, "Operator says it is a number" )
        self.assertFalse( node.is_implicit_multiplicand, "Operator says it can be implicitly mutliplied" )
        self.assertFalse( node.is_implicit_addend, "Operator says it can be implicitly added" )
        self.assertFalse( node.is_inequality, "+ Operator says it is an equality or inequality operator" )
        
    def test_row_1(self):
        node = et.fromstring( XML_1, self.parser )
        self.assertIsInstance( node, MathmlMath, "Didn't get correct type for <math> element: " )
        sympy = node.to_sympy()
        self.assertEquals( sympy.get_sympy_text(), "Le(1*x,3)" )
         
    def test_process_mathml_data_1(self):
        answers = process_mathml_data( XML_1 )
        self.assertEquals( len( answers ), 1 )
        math_expression = answers[0]
        equations = math_expression.sympy_response
        self.assertEquals( len( equations ), 1 )
        self.assertEquals( equations[0], "Le(1*x,3)" )
        node = math_expression.math_node
        self.assertIsInstance( node, MathmlMath )

    