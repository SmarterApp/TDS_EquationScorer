#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

from airscore.eqscorer import evaluateOptions, isEquivalent
from sympy import sympify, solve, Symbol, gcd, Float, Wild
from sympy.parsing.sympy_parser import parse_expr

# Used in tests
def hasEquivalentSolutions(response, rubric, variable = ""):
    if variable == "":
        return solve(sympify(response, evaluateOptions)) == solve(sympify(rubric, evaluateOptions))
    else:
        return solve(sympify(response, evaluateOptions), sympify(variable, evaluateOptions)) == solve(sympify(rubric, evaluateOptions), sympify(variable, evaluateOptions))

# Used in tests
#Returns true if num/det is a reduced fraction
def isReducedFraction(num, det):
    #gcd(num, det, extension=True) factors rational exponents
    return (gcd(num, det) == 1 and sympify(num+'/'+det, evaluateOptions).atoms(Float) == set([]))

# Used in tests
# Matches expression to a pattern in a rubric, returns a set of expressions
# parameters = ['a','b']; variables = ['t','x'];
def matchExpression(response, rubric, parameters, constraints, variables):
    response_expr = sympify(response,evaluateOptions)
    rubric_expr = sympify(rubric, evaluateOptions)
    
    pvariables = []
    for vr in variables:
        pvariables.append(Symbol(vr))

    for ind, par in enumerate(parameters):
        constraints_expr = parse_constraints(constraints, par)
        rubric_expr = rubric_expr.subs(sympify(par), Wild(par, exclude=pvariables, properties=constraints_expr))
    
    retset = []
    if isinstance(response_expr, list):
        return retset

    dict1 = {}
    try:
        dict1 = bestMatch(response_expr, rubric_expr, pvariables)
    except:
        pass

    if dict1:
        for par in parameters:
            prfound = False
            for ky, vr in dict1.iteritems():
                if (ky.name == par) and (vr is not None):
                    atmset = vr.atoms(Symbol)
                    #replacing _ai and _mi for each of the matched subexpressions
                    #if there are more than one occurrence of _ai or _mi, match is not valid
                    for atm in atmset:
                        try:
                            if (atm.name.startswith('_a')):
                                vr = vr.subs(atm,0)
                                break
                        except:
                            pass
                    atmset = vr.atoms(Symbol)
                    for atm in atmset:
                        try:
                            if (atm.name.startswith('_m')):
                                vr = vr.subs(atm,1)
                                break
                        except:
                            pass
                    atmset = vr.atoms(Symbol)
                    for atm in atmset:
                        try:
                            if (atm.name.startswith('_a') or atm.name.startswith('_m')):
                                return [] #invalidate the match
                        except:
                            pass
                    retset.append(str(vr))
                    prfound = True
                    break
            if (not prfound):
                retset.append('')

    return retset

# Used in tests
def bestMatch(response, rubric, var):
    m = response.match(rubric)
    if (m):
        return m

    #find factors of x
    ret = {}
    if len(var) == 1 and rubric.is_Add and response.is_Add and len(rubric.args) == len(response.args):
        for a in rubric.args:
            t1 = a.as_independent(var[0])
            amatched = False
            for b in response.args:
                t2 = b.as_independent(var[0])
                if (t1[1] == t2[1]):
                    ret.update(t2[0].match(t1[0]))
                    amatched = True
                    break

    elif len(var) == 1 and rubric.is_Equality and response.is_Equality:
        #making sure we match everything even if a subexpression does not contain wildcards
        if rubric.lhs.atoms(Wild) == set([]):
            atmset = response.lhs.atoms(Symbol)
            for atm in atmset:
                try:
                    if (atm.name.startswith('_a')):
                        response = response.subs(atm,0)
                    elif (atm.name.startswith('_m')):
                        response = response.subs(atm,1)
                except:
                        pass
            if not isEquivalent(response.lhs, rubric.lhs):
                return ret

        if rubric.rhs.atoms(Wild) == set([]):
            atmset = response.rhs.atoms(Symbol)
            for atm in atmset:
                try:
                    if (atm.name.startswith('_a')):
                        response = response.subs(atm,0)
                    elif (atm.name.startswith('_m')):
                        response = response.subs(atm,1)
                except:
                        pass
            if not isEquivalent(response.rhs, rubric.rhs):
                return ret

        ret.update(bestMatch(response.args[0], rubric.args[0], var))
        ret.update(bestMatch(response.args[1], rubric.args[1], var))

    return ret

# Used in tests
#turns a list ['a > 2 and a <= 4', 'b > 1 or b < 8', 'c != 3', 'd == 2 or d == 4']
#into a list [(lambda a: (a > 2 and a<=4))] for parname='a', or into [(lambda b: (b>1 or b<8))] for parname='b'
def parse_constraints(constraints, parname):
    ret = []

    try:
        for constraint in constraints:
            #find out if parname is mentioned in this constraint
            basicconstraint = constraint
            for allowedsymbol in ['and', 'or', '<', '<=', '>', '>=', '==', '!=']:
                basicconstraint = ' '.join(basicconstraint.split(allowedsymbol))
            if parname in basicconstraint.split():
                ret.append(parse_expr('lambda '+parname+': ('+constraint+')', {'and':'and', 'or':'or', parname:parname}))
    except:
        pass
    
    return ret

