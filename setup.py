#!/usr/bin/env python

from distutils.core import setup

setup(
     name='air_eqscorer',
     version='0.9.2',
     description='AIR Equation Scoring Engine',
     author='American Institutes for Research',
     url='https://bitbucket.org/sbacoss/equationscorer/wiki/Home',
     packages=[
          'airscore',
          'airscore.mathmlsympy',
          'airscore.test',
          'airscore.mathmlsympy.test',
          'eqscorer_rest'
     ],
     package_dir={
          'airscore' : 'lib/airscore',
          'eqscorer_rest' : 'eqscorer_rest/eqscorer_rest'
     },
    )
