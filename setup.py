#!/usr/bin/env python

from setuptools import setup

setup(
     name='air_eqscorer',
     version='0.9.2',
     license='AMERICAN INSTITUTES FOR RESEARCH OPEN SOURCE SOFTWARE LICENSE Version 1.0',
     description='AIR Equation Scoring Engine',
     long_description='An open-source, open-license equation scorer',
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
     install_requires=[
          'sympy >= 0.7.2'
     ],
    )
