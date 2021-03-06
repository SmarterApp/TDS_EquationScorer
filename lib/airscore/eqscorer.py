#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from sympy import expand, nsimplify, simplify, sympify, solve, Equality, Symbol, symbols, gcd, Float, Wild
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import parse_expr

__max_expr_len__ = 500

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = symbols('a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z')
_a1, _a2, _a3, _a4, _a5, _a6, _a7, _a8, _a9, _a10, _a11, _a12, _a13, _a14, _a15, _a16, _a17, _a18, _a19, _a20, _a21, _a22, _a23, _a24, _a25, _a26, _a27, _a28, _a29, _a30, _a31, _a32, _a33, _a34, _a35, _a36, _a37, _a38, _a39, _a40 = symbols('_a1, _a2, _a3, _a4, _a5, _a6, _a7, _a8, _a9, _a10, _a11, _a12, _a13, _a14, _a15, _a16, _a17, _a18, _a19, _a20, _a21, _a22, _a23, _a24, _a25, _a26, _a27, _a28, _a29, _a30, _a31, _a32, _a33, _a34, _a35, _a36, _a37, _a38, _a39, _a40')
_m1, _m2, _m3, _m4, _m5, _m6, _m7, _m8, _m9, _m10, _m11, _m12, _m13, _m14, _m15, _m16, _m17, _m18, _m19, _m20, _m21, _m22, _m23, _m24, _m25, _m26, _m27, _m28, _m29, _m30, _m31, _m32, _m33, _m34, _m35, _m36, _m37, _m38, _m39, _m40 = symbols('_m1, _m2, _m3, _m4, _m5, _m6, _m7, _m8, _m9, _m10, _m11, _m12, _m13, _m14, _m15, _m16, _m17, _m18, _m19, _m20, _m21, _m22, _m23, _m24, _m25, _m26, _m27, _m28, _m29, _m30, _m31, _m32, _m33, _m34, _m35, _m36, _m37, _m38, _m39, _m40')

evaluateOptions = {'evaluate':'evaluate','C':c,'N':n,'Q':q,'S':s}

def isEquivalent(response, rubric, allowChangeOfVariable = False, allowSimplify = True,
                 trigIdentities = False, logIdentities = False, forceAssumptions = False):
    """True if Sympy is able to determine that the two expressions are equivalent.
    
    This function requires two parameters: a test answer and a rubric. Each of these
    is a string. Each string defines an equality, an inequality, or an expression in
    a form that can be parsed by the Sympy symbolic mathematics library. Alternatively,
    the answer or rubric may be a list of such equations, inequalities or expressions,
    enclosed in square brackets and separated by commas.
    
    Additional optional parameters control the manipulations that Sympy will make when
    attempting to determine the equivalence of the response and the rubric
    
    :param response: The test response
    
    :type response: str
    
    :param rubric: The rubric for the test questions
    
    :type rubric: str
    
    :param allowChangeOfVariables:
    
    :type allowChangeOfVariables: bool

    :param allowSimplify:
    
    :type allowSimplify: bool

    :param trigIdentities:
    
    :type trigIdentities: bool

    :param logIdentities:
    
    :type logIdentities: bool

    :param forceAssumptions:
    
    :type forceAssumptions: bool

    """
    response_expr = sympify(response, evaluateOptions)
    rubric_expr = sympify(rubric, evaluateOptions)
    
    #sympy forces simplification of arithmetic (in)equailities into True or False
    if isinstance(response_expr, bool) or isinstance(rubric_expr, bool):
        #manually extract lhs and rhs from rubric and response
        response_ineq = isInequality(response)
        rubric_ineq = isInequality(rubric)
        if (isinstance(response_expr, bool) and response_ineq[0] > -1 or isinstance(rubric_expr, bool) and rubric_ineq[0] > -1):
            if (not response_ineq[0] > -1 or not rubric_ineq[0] > -1 or response_ineq[0] != rubric_ineq[0]):
                return False
            if (response_ineq[0] == 0 or response_ineq[0] == 1):
                #allow commutation
                return isEquivalent(response_ineq[1], rubric_ineq[1], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and \
                    isEquivalent(response_ineq[2], rubric_ineq[2], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions) or \
                    isEquivalent(response_ineq[1], rubric_ineq[2], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and \
                    isEquivalent(response_ineq[2], rubric_ineq[1], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions)
        
            return isEquivalent(response_ineq[1], rubric_ineq[1], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and \
                isEquivalent(response_ineq[2], rubric_ineq[2], False, allowSimplify, trigIdentities, logIdentities, forceAssumptions)
        
        if (isinstance(response_expr, bool) and isinstance(rubric_expr, bool)):
            return (response_expr == rubric_expr)
        else:
            return False
        
    elif (isinstance(response_expr, Equality) or isinstance(rubric_expr, Equality)):
        if (isinstance(rubric_expr, Equality) and isinstance(response_expr, Equality)):
            if allowSimplify:
                return (findFactor(response_expr.rhs - response_expr.lhs, rubric_expr.rhs - rubric_expr.lhs) != None)
            else:
                return (isEquivalentExpressions(response_expr.rhs, rubric_expr.rhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and  isEquivalentExpressions(response_expr.lhs, rubric_expr.lhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) or \
                       isEquivalentExpressions(response_expr.lhs, rubric_expr.rhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and  isEquivalentExpressions(response_expr.rhs, rubric_expr.lhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions))
        else:
            return False            
    elif (isinstance(rubric_expr, list) or isinstance(response_expr, list)):
        if (isinstance(rubric_expr, list) and isinstance(response_expr, list)):
            return (response_expr == rubric_expr)
        else:
            return False
    elif (isinstance(rubric_expr, tuple) or isinstance(response_expr, tuple)):
        if (isinstance(rubric_expr, tuple) and isinstance(response_expr, tuple)):
            return (response_expr == rubric_expr)
        else:
            return False
    return isEquivalentExpressions(response_expr, rubric_expr, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions)

def isEquivalentExpressions(response, rubric, allowChangeOfVariable = False, allowSimplify = True, trigIdentities = False, logIdentities = False, forceAssumptions = False):
    if not allowChangeOfVariable:
        if isinstance(response, bool):
            return (type(response) == type(rubric) and response == rubric)
        elif trigIdentities:
            return simplify(expand(nsimplify(response - rubric, rational=True), trig=True)) == 0 
        elif logIdentities and forceAssumptions:
            return simplify(expand(nsimplify(response - rubric, rational=True), log=True, force=True)) == 0 
        elif logIdentities:
            return simplify(expand(nsimplify(response - rubric, rational=True), log=True)) == 0 
        elif allowSimplify:
            return simplify(nsimplify(response - rubric, rational=True)) == 0
        else:
            return response == rubric
    if len(response.free_symbols) == 0:
        return isEquivalent(response, rubric)
    if len(response.free_symbols) > 1:
        raise Exception("Don't know how to test change of variable equivalence of 2 expressions if they have more than 1 variable. Yet")
    if len(response.free_symbols) != len(rubric.free_symbols):
        return False
    return isEquivalent(response.subs(response.free_symbols.pop(),rubric.free_symbols.pop()), rubric)

def isInequality(exprstr):
    if (len(exprstr) < 5 or not exprstr[0:3] in ('Eq(','Le(','Lt(','Ge(','Gt(','Ne(') or not exprstr.endswith(')')):
        return -1, None, None
    indlhs = exprstr.find(',')
    if (not indlhs > -1 or parsable(exprstr[3:indlhs]) or parsable(exprstr[indlhs+1:-1])):
        return -1, None, None
    eqtype = exprstr[0:3]
    if (eqtype == 'Eq('):
        return 0, exprstr[3:indlhs], exprstr[indlhs+1:-1]
    if (eqtype == 'Ne('):
        return 1, exprstr[3:indlhs], exprstr[indlhs+1:-1]
    if (eqtype == 'Le('):
        return 2, exprstr[3:indlhs], exprstr[indlhs+1:-1]
    if (eqtype == 'Ge('):
        return 2, exprstr[indlhs+1:-1], exprstr[3:indlhs]
    if (eqtype == 'Lt('):
        return 3, exprstr[3:indlhs], exprstr[indlhs+1:-1]
    if (eqtype == 'Gt('):
        return 3, exprstr[indlhs+1:-1], exprstr[3:indlhs]


# Check if exp1 = f*exp2 for f=1 or -1
def findFactor(exp1, exp2):
    ret = None
    if (isEquivalentExpressions(exp1, exp2)):
        ret = 1
    elif (isEquivalentExpressions(exp1, -1*exp2)):
        ret = -1
    else:
        try:
            for it in xrange(27):
                smbl = Symbol(chr(ord('a')+it))
                if smbl not in exp1.atoms(Symbol) and smbl not in exp2.atoms(Symbol):
                    break

            if smbl not in exp1.atoms(Symbol) and smbl not in exp2.atoms(Symbol):
                sol = solve(exp1 - smbl*exp2, smbl)
                if sol and len(sol[0].atoms(Symbol)) == 0:
                    ret = sol[0]
        except:
            #solver was not successful
            pass

    return ret


def parsable(response):
    try:
        if (len(response) > __max_expr_len__):
            raise ValueError("Expression is too long")
        sympify(response, evaluateOptions)
    except (SympifyError, TypeError, AttributeError, ZeroDivisionError, ValueError):
        return 1
    else:
        return 0 

