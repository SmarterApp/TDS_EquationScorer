#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from xml.etree import ElementTree as et

from airscore.mathmlsympy.parser import process_mathml_data, MATHML_NAMESPACE
from airscore.mathmlsympy.mathml_containers import MathmlMath, MathmlMStyle, MathmlMRow
from airscore.mathmlsympy.mathml_number import MathmlMN
from airscore.mathmlsympy.mathml_identifier import MathmlMI
from airscore.mathmlsympy.mathml_operators import MathmlMO, Inequality
from airscore.mathmlsympy.substitutions import DICTIONARY
import abstract_parser_test

class TestParser( abstract_parser_test.TestCase ):
    
    def test_build_tree(self):
        tree = et.fromstring( abstract_parser_test.XML_1, self.parser )
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
        
    def test_number_3(self):
        '''Dots are parts of numbers, even if listed as operators
        '''
        node = et.fromstring( abstract_parser_test.XML_2, self.parser )
        txt = node.get_sympy_text()
        self.assertEquals( txt, '(5.0)', "Got the wrong content from the sympy linked list: " + txt )

    def test_number_4(self):
        '''Dots are numbers
        '''
        node = et.fromstring( '<mo xmlns="http://www.w3.org/1998/Math/MathML">.</mo>', self.parser )
        self.assertIsInstance( node, MathmlMN, "Didn't get correct type for <mo>.</mo> element: " )
        
    def test_number_5(self):
        '''Simple integer
        '''
        xml = self.mathml_wrap('<mn>123</mn>')
        tree = et.fromstring( xml, self.parser )
        node = tree[0][0]
        self.assertIsInstance( node, MathmlMN, "Didn't get correct type for <mn> element: " )
        self.assertTrue( node.is_non_neg_integer )
        
    def test_number_6(self):
        '''Simple number not an integer
        '''
        xml = self.mathml_wrap('<mn>123.4</mn>')
        tree = et.fromstring( xml, self.parser )
        node = tree[0][0]
        self.assertIsInstance( node, MathmlMN, "Didn't get correct type for <mn> element: " )
        self.assertFalse( node.is_non_neg_integer )
        
        
    def test_number_7(self):
        '''Negatibve number not an integer
        '''
        xml = self.mathml_wrap('<mn>-123</mn>')
        tree = et.fromstring( xml, self.parser )
        node = tree[0][0]
        self.assertIsInstance( node, MathmlMN, "Didn't get correct type for <mn> element: " )
        self.assertFalse( node.is_non_neg_integer )
        
        
    def test_number_8(self):
        '''Compound integer
        '''
        xml = self.mathml_wrap('<mrow><mn>123</mn><mn>456</mn></mrow>')
        tree = et.fromstring( xml, self.parser )
        node = tree[0][0]
        self.assertIsInstance( node, MathmlMRow, "Didn't get correct type for <mn> element: " )
        self.assertTrue( node.is_non_neg_integer )
        
        
    def test_number_9(self):
        '''Compound number not an integer
        '''
        xml = self.mathml_wrap('<mrow><mn>123</mn><mo>+</mo><mn>456</mn></mrow>')
        tree = et.fromstring( xml, self.parser )
        node = tree[0][0]
        self.assertIsInstance( node, MathmlMRow, "Didn't get correct type for <mn> element: " )
        self.assertFalse( node.is_non_neg_integer )
        
    def test_number_10(self):
        '''Implicit addition for mixed fractions
        '''
        xml = self.mathml_wrap('<mn>1</mn><mfrac><mrow><mn>123</mn></mrow><mrow><mn>456</mn></mrow></mfrac>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "1+(123)/(456)"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
    def test_number_11(self):
        '''Revert to multiplication if fraction is not a simple ratio of non-negative integers
        '''
        xml = self.mathml_wrap('<mn>1</mn><mfrac><mrow><mn>1</mn></mrow><mrow><mi>x</mi></mrow></mfrac>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "1*(1)/(x)"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
        
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
        
    def test_identifier_3(self):
        '''Suppress implicit multiplication between a function and an identifier
        '''
        xml = self.mathml_wrap('<mn>3</mn><mi>cos</mi><mo>(</mo><mi>y</mi><mo>)</mo>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "3*cos(y)"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
    def test_identifier_4(self):
        '''MText is treated as an identifier
        '''
        node = et.fromstring( '<mtext xmlns="http://www.w3.org/1998/Math/MathML">bob</mtext>', self.parser )
        self.assertIsInstance( node, MathmlMI, "Didn't get correct type for <mtext> element: " )
        self.assertEquals( node.get_sympy_text(), 'bob', "Got the wrong content in the XML node" )
        self.assertFalse( node.is_number, "Identifier says it is a number" )
        self.assertTrue( node.is_implicit_multiplicand, "Identifier says it cannot be implicitly mutliplied" )
        self.assertFalse( node.is_implicit_addend, "Identifier says it can be implicitly added" )
        self.assertFalse( node.is_inequality, "Identifier says it is an equality or inequality operator" )
        sympy = node.to_sympy()
        self.assertEquals( sympy.get_sympy_text(), 'bob', "Got the wrong content from the sympy linked list" )
        
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
        """Are inequqlity operators being created with the inequality class?
        """
        operators = { u'&lt;':u'Lt', u'\u2264':u'Le', u'=':u'Eq', u'\u2265':u'Ge', u'&gt;':u'Gt', u'>':u'Gt'  }
    
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
        """Are non-inequqlity operators not being created with the inequality class?
        """
        node = et.fromstring( '<mo xmlns="http://www.w3.org/1998/Math/MathML">+</mo>',
                                self.parser )
        self.assertFalse( isinstance( node, Inequality ), "Thinks <mo>+</mo> element os an inequality" )
        self.assertIsInstance( node, MathmlMO, "Didn't get correct type for <mo>+</mo> element" )
        self.assertEquals( node.get_sympy_text(), '+', "Got the wrong content in the XML node" )
        self.assertFalse( node.is_number, "Operator says it is a number" )
        self.assertFalse( node.is_implicit_multiplicand, "Operator says it can be implicitly mutliplied" )
        self.assertFalse( node.is_implicit_addend, "Operator says it can be implicitly added" )
        self.assertFalse( node.is_inequality, "+ Operator says it is an equality or inequality operator" )
        
    def test_operators_3(self):
        """Support implicit multiplication before and after grouping operators
        """
        xml = self.mathml_wrap('<mn>3</mn><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "3*(x)*y"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
    def test_operators_4(self):
        """Pipes converted into absolute value function calls
        """
        xml = self.mathml_wrap('<mo>|</mo><mi>x</mi><mo>|</mo><mo>+</mo><mo>|</mo><mi>y</mi><mo>|</mo>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "Abs(x)+Abs(y)"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
    def test_operators_5(self):
        """Absolute value correctly supports implicit multiplication before and after
        """
        xml = self.mathml_wrap('<mn>3</mn><mo>|</mo><mi>x</mi><mo>|</mo><mi>y</mi>')
        node = et.fromstring( xml, self.parser )
        txt = node.get_sympy_text()
        archetype = "3*Abs(x)*y"
        self.assertEquals( txt, archetype, 'Found {!r}, expected {!r}'.format( txt, archetype ) )
        
    def test_row_1(self):
        """Are we correctly parsing a whole equation?
        """
        node = et.fromstring( abstract_parser_test.XML_1, self.parser )
        self.assertIsInstance( node, MathmlMath, "Didn't get correct type for <math> element: " )
        sympy = node.to_sympy()
        self.assertEquals( sympy.get_sympy_text(), "Le(1*x,3)" )
         
    def test_row_2(self):
        """What do we do with an expression with no equality or inequality operators?
        """
        xml = self.mathml_wrap( u'<mn>7</mn><mi>x</mi>' )
        node = et.fromstring( xml, self.parser )
        self.assertIsInstance( node, MathmlMath, "Didn't get correct type for <math> element: " )
        archetype = "7*x"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )
         
    def test_process_mathml_data_1(self):
        """Test the process_mathml_data wrapper function
        """
        answers = process_mathml_data( abstract_parser_test.XML_1 )
        self.assertEquals( len( answers ), 1 )
        math_expression = answers[0]
        equations = math_expression.sympy_response
        self.assertEquals( len( equations ), 1 )
        self.assertEquals( equations[0], "Le(1*x,3)" )
        node = math_expression.math_node
        self.assertIsInstance( node, MathmlMath )

    def test_substitutions(self):
        """Are the XML objects correctly decoding the dictionary words?
        """
        for from_, to in DICTIONARY.iteritems():
            xml = u'<?xml version="1.0" encoding="UTF-8"?><mo xmlns="{ns}">{txt}</mo>'.format( ns=MATHML_NAMESPACE, txt=from_ ).encode('utf-8')
            node=et.fromstring( xml, self.parser )
            txt = node.decoded_text
            self.assertEquals( txt, to, u"decoded_text returned {!r} instead of {!r}".format( txt, to ) )
            # Pipe operator has special handling for get_sympy_text()
            if to != u'|':
                sympy = node.to_sympy()
                txt = sympy.get_sympy_text()
                self.assertEquals( txt, to, u"sympy.get_sympy_text() returned {!r} instead of {!r}".format( txt, to ) )
                
    def test_frac_1(self):
        """A simple (albeit infinite) fraction?
        """
        xml = self.mathml_wrap( u'<mfrac><mrow><mn>1</mn></mrow><mrow><mn>0</mn></mrow></mfrac>' )
        node = et.fromstring( xml, self.parser )
        archetype = "(1)/(0)"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_fenced(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<mfenced open="!@(" close=")@!"><mi>zoggart!</mi></mfenced>' )
        node = et.fromstring( xml, self.parser )
        archetype = "!@(zoggart!)@!"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_sqrt(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<msqrt><mi>zoggart!</mi></msqrt>' )
        node = et.fromstring( xml, self.parser )
        archetype = "sqrt(zoggart!)"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_root(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<mroot><mi>zoggart</mi><mn>3</mn></mroot>' )
        node = et.fromstring( xml, self.parser )
        archetype = "(zoggart)**(1/(3))"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_sup(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<msup><mi>zoggart</mi><mn>3</mn></msup>' )
        node = et.fromstring( xml, self.parser )
        archetype = "(zoggart)**(3)"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_sub(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<msub><mi>zoggart</mi><mn>3</mn></msub>' )
        node = et.fromstring( xml, self.parser )
        archetype = "zoggart_3"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )

    def test_sub_sup(self):
        """Configurable parentheses
        """
        xml = self.mathml_wrap( u'<msubsup><mi>zoggart</mi><mi>j</mi><mn>3</mn></msubsup>' )
        node = et.fromstring( xml, self.parser )
        archetype = "(zoggart_j)**(3)"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, "Saw {}, expected {}".format( txt, archetype ) )
        
    def test_weird_character(self):
        """What happens when our equation contains a character that isn't one of the encodings
        that we've programmed for
        """
        
        not_equal = u'\u2260'
        xml = self.mathml_wrap( u'<mi>x</mi><mo>{}</mo><mi>y</mi>'.format( not_equal ) )
        node = et.fromstring( xml, self.parser )
        archetype = u"x{}y".format( not_equal )
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, u"Saw {}, expected {}".format( txt, archetype ) )
        
        archetype = ( u'['+archetype+']' ).encode( 'UTF-8' )
        fully_processed = str( process_mathml_data( xml ) )
        self.assertEquals( fully_processed, archetype, u"Saw {}, expected {}".format( fully_processed, archetype ) )
        
        
    def test_complex_expression(self):
        xml = self.mathml_wrap( u"<mfenced><mn>4.15</mn><msup><mrow><mn>10</mn></mrow><mrow><mn>2</mn><msup><mrow><mn>20</mn></mrow><mrow><mn>2</mn><mo>+</mo><mn>500</mn></mrow></msup></mrow></msup></mfenced>")
        node = et.fromstring( xml, self.parser )
        archetype = u"(4.15*((10))**((2*((20))**((2+500)))))"
        txt = node.get_sympy_text()
        self.assertEquals( txt, archetype, u"Saw {}, expected {}".format( txt, archetype ) )

