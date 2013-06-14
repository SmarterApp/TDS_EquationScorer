########################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR%20Open%20Source%20License%201.0
########################################################################################

from django.conf.urls import patterns, url
import isequivalent

urlpatterns = patterns('',
    url(r'^isequivalent$', isequivalent.IsEquivalent.as_view()),
)