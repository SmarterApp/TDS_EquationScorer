#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

import time
import unittest
from airscore import Timeout, TimeoutError

class TimeoutTest( unittest.TestCase ):
    def test_timeout( self ):
        try:
            with Timeout(1):
                print 1
                time.sleep(3)
                self.fail( "Execution of sleep was not interrupted" )
        except TimeoutError:
            # SUCCESS!
            return
        self.fail( "Execution of sleep was not interrupted" )
        