###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from parser import mathml_element
from base_mathml_element import BaseMathmlElement

@mathml_element( 'mi' )
class MathmlMI( BaseMathmlElement ):
    pass
