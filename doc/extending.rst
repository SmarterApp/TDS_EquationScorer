.. Copyright (c) 2013 American Institutes for Research
   Distributed under the AIR Open Source License, Version 1.0
   See accompanying file AIR-License-1_0.txt or at 
   https://bitbucket.org/sbacoss/equactionscorer/wiki/AIR_Open_Source_License_1.0

Extending the AIR Equation Scoring Engine
=========================================

.. contents:: Contents
   :local:

The :program:`AIR Equation Scoring Engine` supports a limited subset of the
`MathML <http://www.w3.org/Math/>`_ standard. The most likely place that users
will want to extend the engine is to implement support for MathML constructs
that are not currently supported. This can be accomplished by writing
subclasses of
:class:`airscore.mathmlsympy.base_mathml_element.BaseMathmlElement` or
:class:`airscore.mathmlsympy.mathml_containers.BaseMathmlContainer`,
and registering the new classes with the parser using the
:func:`airscore.mathmlsympy.parser.mathml_element`
decorator.  The interfaces for the relevant classes and methods are described
below.

.. module:: airscore.mathmlsympy.base_mathml_element

:class:`BaseMathmlElement`
++++++++++++++++++++++++++
.. autoclass:: BaseMathmlElement
    :members:

.. module:: airscore.mathmlsympy.mathml_containers

:class:`BaseMathmlContainer`
++++++++++++++++++++++++++++
.. autoclass:: BaseMathmlContainer
    :members:

.. module:: airscore.mathmlsympy.parser
   :noindex:

:func:`mathml_element`
++++++++++++++++++++++
.. autofunction:: mathml_element

.. module:: airscore.mathmlsympy.partial_sympy_object

:class:`PartialSympyObject`
++++++++++++++++++++++++++++
.. autoclass:: PartialSympyObject
  :members:
  