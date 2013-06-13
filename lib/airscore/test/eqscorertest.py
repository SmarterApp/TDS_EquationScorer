########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

import unittest

from airscore.eqscorer import isEquivalent
from sympy import S

class EqScorerTest( unittest.TestCase ):
#tests to remain valid after implementation change
        
    def eqtestlib( self ):
        #numbers (integers, floats, operators +-*/,)
        assert isEquivalent('2', '1+1')
        assert not isEquivalent('2', '1')
        assert isEquivalent('2.1', '0.21e+1')
        assert isEquivalent('1/3', '2/6')
        assert not isEquivalent('1/3', '0.333')
        assert isEquivalent('2', '2.0')
        #arithmetic equalities
        assert isEquivalent('Eq(1,5-4+3-2-1)','Eq(1,1)', allowSimplify = True)
        #assert not isEquivalent('Eq(1,5-4+3-2-1)','Eq(1,1)', allowSimplify = False)
        assert isEquivalent('Eq(1,1)', 'Eq(1,5-4+3-2-1)', allowSimplify = True)
        #assert not isEquivalent('Eq(1,1)', 'Eq(1,5-4+3-2-1)', allowSimplify = False)
        assert not isEquivalent('Eq(1,5-4+3-2-1)','True')
        assert not isEquivalent('True', 'Eq(1,5-4+3-2-1)')
        assert isEquivalent('True', 'True')
        assert isEquivalent('False', 'False')
        assert not isEquivalent('True', 'False')
        assert not isEquivalent('Eq(2,1)','Eq(3,2)')
        assert isEquivalent('Eq(2,1)','Eq(2,1)')
        assert isEquivalent('Eq(2,1)','Eq(1,2)')
        assert isEquivalent('Eq(1+1,1)','Eq(1,2)')
        assert isEquivalent('Ne(2,1)','Ne(2,1)')
        assert isEquivalent('Ne(2,1)','Ne(1,2)')
        assert isEquivalent('Le(1,2)','Le(1,2)')
        assert isEquivalent('Ge(2,1)','Le(1,2)')
        assert isEquivalent('Ge(1+1,1)','Le(1,2)')
        assert not isEquivalent('Ge(3,1)','Le(1,2)')
        assert not isEquivalent('Ge(1+1+1,1)','Le(1,2)')
        assert not isEquivalent('Le(1,2)','Lt(1,2)')
        assert isEquivalent('Lt(1,2)','Lt(1,2)')
        assert isEquivalent('Gt(2,1)','Lt(1,2)')
        #parse correctly evaluate keyword used for disabling auto simplifications
        assert isEquivalent('Eq(x,1)','Eq(x,Add(2,-1,evaluate=True))')
        #reloaded division operator to float division
        assert isEquivalent('Eq(x,0.5)', 'Eq(x,1/2)')
        assert isEquivalent('x**(1/2)','x**0.5')
        #multiplication expansion
        assert isEquivalent('a*(a+b)', 'a**2+a*b', allowSimplify = True)
        assert isEquivalent('a*(a+b)', 'a**2.0+a*b', allowSimplify = True)
        assert not isEquivalent('a*(a+b)', 'a**2+a*b', allowSimplify = False)
        assert isEquivalent('Eq(y,x**2-6*x+5)', 'Eq(y,(x-1)*(x-5))', allowSimplify = True)
        assert not isEquivalent('Eq(y,x**2-6*x+5)', 'Eq(y,(x-1)*(x-5))', allowSimplify = False)
        assert isEquivalent('Eq(y,(x-1)*(x-5))', 'Eq(x**2-6*x+5,y)', allowSimplify = True)
        assert not isEquivalent('Eq(y,(x-1)*(x-5))', 'Eq(x**2-6*x+5,y)', allowSimplify = False)
        assert isEquivalent('Eq(a,2*b+1)','Eq(4*b+2,2*a)') 
        assert not isEquivalent('Eq(a,2*b+1)','Eq(4*b+2,2*a+1)')
        #Trig functions and identities
        assert isEquivalent('cos(t)', 'sin(t+pi/2)')
        assert isEquivalent('cos(t+pi/2)', '-sin(t)')
        assert isEquivalent('sin(2*x)','2*sin(x)*cos(x)',trigIdentities=True) 
        assert isEquivalent('cos(2*x)','1-2*sin(x)**2',trigIdentities=True)
        assert isEquivalent('cos(x/0.5)','1-2*sin(x)**2',trigIdentities=True)
        assert isEquivalent('sin(x)**2+cos(x)**2', '1')
        #Log functions and identities
        assert isEquivalent('exp(2*x)','(exp(x))**2')
        assert isEquivalent('exp(ln(x))','x')
        assert isEquivalent('log(x**2)','2*log(x)',logIdentities=True,forceAssumptions=True)
        
    
    def bugfixtest( self ):
        print "stack overflow test"
        S('Eq(64.80,16.20*f((15.50/1.00)))')
        print "sub bool test"
        assert not isEquivalent('Eq(3,s)', 'Le(3,4)')
        assert not isEquivalent('Le(3,s)', 'Le(3,4)')
    
