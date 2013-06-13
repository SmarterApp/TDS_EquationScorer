###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from messages import IsEquivalentRequest, IsEquivalentResponse

class RequestSerializer( serializers.Serializer ):
    rubric = serializers.CharField( required=True, source='rubric' )
    answer = serializers.CharField( required=True, source='answer' )
    parameters = serializers.WritableField( required=False, source='parameters' )
    
    def restore_object( self, attrs, instance=None ):
        if instance is not None:
            instance.rubric = attrs.get( 'rubric', instance.rubric )
            instance.answer = attrs.get( 'answer', instance.answer )
            params = attrs.get( 'parameters', None )
            if params is not None:
                try:
                    instance.parameters = instance.Parameters( **params )
                except Exception:
                    raise ParseError( detail="Illegal values for 'parameters'" )
            return instance
        return IsEquivalentRequest( **attrs )
    
                
class ResponseSerializer( serializers.Serializer ):
    correct = serializers.BooleanField( required=True, source='correct' )
    reason = serializers.CharField( required=False, source='reason' )
    
    def restore_object( self, attrs, instance=None ):
        if instance is not None:
            instance.correct = attrs.get( 'correct', instance.correct )
            instance.reason = attrs.get( 'reason', instance.reason )
            return instance
        return IsEquivalentResponse( **attrs )
