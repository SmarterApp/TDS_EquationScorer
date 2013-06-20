.. Copyright (c) 2013 American Institutes for Research
   Distributed under the AIR Open Source License, Version 1.0
   See accompanying file AIR-License-1_0.txt or at 
   https://bitbucket.org/sbacoss/equation_scorer/wiki/AIR_Open_Source_License_1.0

AIR Equation Scoring Engine Python API
======================================
.. contents:: Contents
   :local:

.. module:: airscore

Module :mod:`airscore`
++++++++++++++++++++++

The :mod:`airscore` module is the primary Python entry point for the :program:`AIR
Equation Scoring Engine`\ .  It provides two functions. The function
:func:`process_mathml_data` accepts inputs in the `MathML
<http://www.w3.org/Math/>`_ format, and returns an equivalent expression in a
form that can be parsed by the `Sympy <http://sympy.org/en/index.html>`_
symbolic mathematics library. The function :func:`isEquivalent` Uses Sympy
to determine if two sets of expressions, equations, or inequalities are
mathematically equivalent.

In order to compare a test answer, expressed in MathML, with a rubric, also
expressed in MathML, the two functions are used in conjunction, like this::

    answer_txt = unicode( process_mathml_data( answer_mathml ) )
    rubric_txt = unicode( process_mathml_data( rubric_mathml ) )
    is_correct = isEquivalent( answer_txt, rubric_txt )
    
.. autofunction:: airscore.isEquivalent

.. autofunction:: airscore.process_mathml_data

Module :mod:`airscore.mathmlsympy.math_expression`
++++++++++++++++++++++++++++++++++++++++++++++++++

.. module:: airscore.mathmlsympy.math_expression

Most of the classes and methods in :mod:`airscore.mathmlsympy.math_expression`
are mainly of interested to those who intend to extend the MathML parsing engine
to understand a wider selection of MathML elements.  Two classes may be of
interest to ordinary users of these libraries, however. These are the
:class:`MathExpressionList` class that is returned by
:func:`airscore.process_mathml_data`, and the :class:`MathExpression` objects that
it contains.

.. autoclass:: MathExpression

.. autoclass:: MathExpressionList

