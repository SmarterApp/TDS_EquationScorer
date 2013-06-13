########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from airscore import isEquivalent, process_mathml_data
from serializers import RequestSerializer, ResponseSerializer
from messages import IsEquivalentRequest, IsEquivalentResponse

class IsEquivalent( APIView ):
    
    def post( self, request, format=None ):
        try:
            ans = self._post( request )
        except ErrorGuard as e:
            return Response( data=ResponseSerializer( e.response ).data,
                             status=e.status_code,
                             exception=e )
        return Response( ResponseSerializer( ans ).data )

    def _post( self, request ):
        serializer = RequestSerializer( instance=IsEquivalentRequest(), data=request.DATA )
        response = IsEquivalentResponse( correct=False, reason='' )
        
        ## It seems completely insane, but the request is deserialized as a side-effect of retrieving the
        ## errors object!
        errors = serializer.errors
        if not errors:
            valid_request = serializer.object
        else:
            response.reason = "Invalid request object"
            raise ErrorGuard( response, None, "Invalid request object", 400 )
        
        with ErrorGuard( response, Exception, "Unable to parse rubric as mathml", 400 ):
            rubric = unicode( process_mathml_data( valid_request.rubric ) )
            
        with ErrorGuard( response, Exception, "Unable to parse answer as mathml", 400 ):
            answer = unicode( process_mathml_data( valid_request.answer ) )

        with ErrorGuard( response, Exception, "Unable to compare answer with rubric", 400 ):
            p = valid_request.parameters
            correct = isEquivalent( answer, rubric,
                    allowChangeOfVariable = p.allow_change_of_variable,
                    allowSimplify = p.allow_simplify,
                    trigIdentities = p.trig_identities,
                    logIdentities = p.log_identities,
                    forceAssumptions = p.force_assumptions )

        response.correct = correct
        if not correct:
            response.reason = "Answer is not equivalent to rubric"
        return response

class ErrorGuard( APIException ):
    '''A context manager that collects an expected error and raises a different error that triggers
    an appropriate HTML response.
    '''
    def __init__( self, response, expected, detail, status_code ):
        self.response = response
        self.expected = expected
        self.exception = None
        self.detail = detail
        self.status_code = status_code
        
    def __enter__( self ):
        pass
    
    def __exit__( self, exc_type, exc_value, traceback ):
        if isinstance( exc_type, self.expected ):
            self.response.reason = self.message
            self.exception = exc_value
            raise self
        return None

