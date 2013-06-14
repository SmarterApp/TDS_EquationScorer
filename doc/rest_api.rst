.. Copyright (c) 2013 American Institutes for Research
   Distributed under the AIR Open Source License, Version 1.0
   See accompanying file AIR-License-1_0.txt or at 
   https://bitbucket.org/sbacoss/eotds/wiki/AIR_Open_Source_License
   
.. |le| unicode:: U+2264

AIR Equation Scoring Engine RESTful Web Interface
=================================================
.. contents:: Contents
   :local:

The REST interface has a single access point.  A ``POST`` to :file:``/isequivalent/``
with a JSON payload, returns a JSON object containing the results of the call.

**POST /isequivalent/**
-----------------------
Test whether an answer is mathematically equivalent to the rubric

Parameters
++++++++++

**answer** (String, required)
  The test answer

  A JSON string containing a MathML expression. Per the JSON specification, all quotation marks within the
  MathML must be preceded by backslashes.
  
  Any "special" characters in the answer may be included in one of three ways:
  
    - They may simply be embedded as unicode in the charset of the request ( e.g., |le| )
    
    - They may be escaped as XML escape sequences ( e.g., ``&#x2264;``)
    
    - They may be escaped as JSON escape sequences (e.g., ``\u2264``)

**rubric** (String, required)
  The rubric against which the answer will be compared.

  A JSON string containing a MathML expression. Per the JSON specification, all quotation marks within the
  MathML must be preceded by backslashes.
  
**parameters** (Dictionary, optional)
  A dictionary of parameters that modify how sympy tests for equivalency. If omitted, all of the parameters
  take on their default values.  The keys permitted in **parameters** are the following:

  **allow_change_of_variable** (``true`` or ``false``, optional)
    Default ``false``
    
  **allow_simplify** (``true`` or ``false``, optional)
    Default ``true``
    
  **trigIdentities** (``true`` or ``false``, optional)
    Default ``false``
    
  **logIdentities** (``true`` or ``false``, optional)
    Default ``false``
    
  **forceAssumptions** (``true`` or ``false``)
    Default ``false``

Normal Return Values
++++++++++++++++++++

**Status**
  200 OK

**Body**
  A JSON dictionary containing two entries

  **correct** (``true`` or ``false``)
    Whether or not the answer was equivalent to the rubric
    
  **reason** (``true`` or ``false``)
    If **correct** was ``true``, then this will be an empty string. Otherwise
    it will describe the reason that the answer was rejected.  This may be
    one of the following
    
      ``Answer is not equivalent to rubric``
        SymPy determined that the answer and the rubric were not equivalent
	
      ``Unable to parse answer as mathml``
        The answer was not valid mathml, or contains mathml constructs
	that are not currently supported by this package.
	
      ``Unable to compare answer with rubric``
        Sympy raised an error while attempting to test the answer and the
	rubric for equivalence

Return on Error
+++++++++++++++
If the **answer** field on the request is not parsable MathML, then a "normal"
return value will be reported, with a status of ``200``, a **correct** value of
``false``, and a **reason** value containing a message describing the reason for
the failure. In all other cases, a non-``2xx`` error status will be returned.

The body of the error response will depend on where in the processing of the
request the error occurred. If an error occurs in the Equation Scorer REST code,
then the response code will be ``400``, and a JSON structure will be returned
identical to the one returned for a "normal" response.

Examples
++++++++

Example 1::

    POST /isequivalent/ HTTP/1.1
    Host: example.com
    Content-Type: application/json; charset=UTF-8
    Accept: application/json
    
    {
      "answer":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>",
      "rubric":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>"
    }

Response 1::

    HTTP/1.0 200 OK
    Date: Thu, 13 Jun 2013 18:27:39 GMT
    Server: WSGIServer/0.1 Python/2.7.4
    Vary: Accept, Cookie
    Content-Type: application/json; charset=utf-8
    Allow: POST, OPTIONS

    {"correct": true, "reason": ""}

Example 2 (Incorrect answer)::

    POST /isequivalent/ HTTP/1.1
    Host: example.com
    Content-Type: application/json; charset=UTF-8
    Accept: application/json
    
    {
      "answer":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>=</mo><mn>3</mn></math>",
      "rubric":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>"
    }

Response 2::

    HTTP/1.0 200 OK
    Date: Thu, 13 Jun 2013 18:27:39 GMT
    Server: WSGIServer/0.1 Python/2.7.4
    Vary: Accept, Cookie
    Content-Type: application/json; charset=utf-8
    Allow: POST, OPTIONS

    {"correct": false, "reason": "Answer is not equivalent to rubric"}

Example 3 (Parameters for equivalence check)::

    POST /isequivalent/ HTTP/1.1
    Host: example.com
    Content-Type: application/json; charset=UTF-8
    Accept: application/json
    
    {
      "answer":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>",
      "rubric":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>",
      "parameters":{ "allow_change_of_variable":true }
    }

Response 3::

    HTTP/1.0 200 OK
    Date: Thu, 13 Jun 2013 18:27:39 GMT
    Server: WSGIServer/0.1 Python/2.7.4
    Vary: Accept, Cookie
    Content-Type: application/json; charset=utf-8
    Allow: POST, OPTIONS

    {"correct": true, "reason": ""}
