########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from sympy import expand, nsimplify, simplify, sympify, solve, Equality, Symbol
from sympy.core.sympify import SympifyError

def isEquivalent(response, rubric, allowChangeOfVariable = False, allowSimplify = True, trigIdentities = False, logIdentities = False, forceAssumptions = False):
    response_expr = sympify(response, {'evaluate':'evaluate'})
    rubric_expr = sympify(rubric, {'evaluate':'evaluate'})
    
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
        
    elif (isinstance(response_expr, Equality) and isinstance(rubric_expr, Equality)):
        if allowSimplify:
            return (findFactor(response_expr.rhs - response_expr.lhs, rubric_expr.rhs - rubric_expr.lhs) != None)
        else:
            return (isEquivalentExpressions(response_expr.rhs, rubric_expr.rhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and  isEquivalentExpressions(response_expr.lhs, rubric_expr.lhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) or \
                       isEquivalentExpressions(response_expr.lhs, rubric_expr.rhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions) and  isEquivalentExpressions(response_expr.rhs, rubric_expr.lhs, allowChangeOfVariable, allowSimplify, trigIdentities, logIdentities, forceAssumptions))
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

# Check if exp1 = f*exp2 for arbitrary f
def findFactor(exp1, exp2):
    ret = None
    for it in xrange(27):
        smbl = Symbol(chr(ord('a')+it))
        if smbl not in exp1.atoms(Symbol) and smbl not in exp2.atoms(Symbol):
            break

    if smbl not in exp1.atoms(Symbol) and smbl not in exp2.atoms(Symbol):
        sol = solve(exp1 - smbl*exp2, smbl)
        if sol and len(sol[0].atoms(Symbol)) == 0:
            ret = sol[0]

    return ret

def parsable(response):
    try:
        sympify(response, {'evaluate':'evaluate'})
    except SympifyError:
        return 1 
    except TypeError:
        return 1
    else:
        return 0 

