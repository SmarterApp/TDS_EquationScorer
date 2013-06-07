###############################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
###############################################################################

from parser import process_mathml_data

# Force the imports to happen so that the classes are appropriately registered
import mathml_containers
import mathml_identifier
import mathml_number
import mathml_operators
import mathml_fraction
import mathml_misc
