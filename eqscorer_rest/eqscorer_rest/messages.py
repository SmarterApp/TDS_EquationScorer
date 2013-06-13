########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

class IsEquivalentRequest( object ):
    def __init__( self, rubric=None, answer=None, parameters={} ):
        self.rubric = rubric
        self.answer = answer
        self.parameters = self.Parameters( **parameters )
        
    class Parameters( object ):
        def __init__( self, allow_change_of_variable = False, allow_simplify = True, trig_identities = False,
                  log_identities = False, force_assumptions = False, **kwargs ):
            self.allow_change_of_variable = allow_change_of_variable
            self.allow_simplify = allow_simplify
            self.trig_identities = trig_identities
            self.log_identities = log_identities
            self.force_assumptions = force_assumptions
        
class IsEquivalentResponse( object ):
    def __init__( self, correct=False, reason=None ):
        self.correct = correct
        self.reason = reason
