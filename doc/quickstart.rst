.. Copyright (c) 2013 American Institutes for Research
   Distributed under the AIR Open Source License, Version 1.0
   See accompanying file AIR-License-1_0.txt or at 
   https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0

Quick Start: REST interface on Apache 2.4 for Windows
=====================================================
.. contents:: Contents
   :local:


This document describes how to get up-and-running with the :program:`AIR Equation Scoring Engine`'s
RESTful web interface on a :program:`Windows` machine running :program:`Apache httpd` version 2.4.

The configuration described herein is meant for testing and development only.
You will probably want to set up something more robust for a production system.

Get the Dependencies
++++++++++++++++++++

You will need to install the :program:`Apache httpd` server. These instructions were
written for version 2.4.4, but they should work with minimal changes for any
version of Apache 2.2 or 2.4. I used the Windows 64 binary build from
`Apache Lounge <http://www.apachelounge.com/>`_
(http://www.apachelounge.com/download/win64/binaries/httpd-2.4.4-win64.zip)

You will need to have the :program:`Python` programming language installed. The
software was developed and tested
on Python 2.7.4 for 64-bit Windows. The software should run fine on any version
of 2.7.  It has not been tested on Python 2.6 or earlier. It will not run on
any version of Python 3

A Windows installer for the latest version of Python may be downloaded from
here: http://www.python.org/download/

I recommend installing Python's :program:`setuptools` (https://pypi.python.org/pypi/setuptools)
and :program:`pip` (https://pypi.python.org/pypi/pip). packages. Once the setuptools are installed,
you can install pip using::

    c:\Python27\Scripts\easy-install pip
    
Then use pip to install the remaining Python dependencies::

    c:\Python27\Scripts\pip install sympy
    c:\Python27\Scripts\pip install django
    c:\Python27\Scripts\pip install djangorestframework
    
An Apache plugin called :program:`mod_wsgi` provides the bridge
between Apache and Python. It is easiest to acquire a pre-compiled binary
for this package. One is available from http://www.lfd.uci.edu/~gohlke/pythonlibs/
Be sure to download the version that is appropriate for your Apache version,
Python version and Windows architecture.  After downloading the zip archive,
extract the single file that it contains (should be called :file:`mod_wsgi.so`) and
drop it into the Apache modules directory (this is :file:`C:\\Program Files\\Apache24\\modules`
on my machine)

Finally, in order to test the setup, you will need some way of sending a **POST**
request to the Apache server.  These instructions assume that you are using the
:program:`Fiddler` utility (http://fiddler2.com/get-fiddler). If you prefer a different
utility, then modify them accordingly.

Download the Software
+++++++++++++++++++++

Download the latest version of the :program:`AIR Equation Scoring Engine` from
https://bitbucket.org/sbacoss/equationscorer/downloads

Unzip the downloaded archive into a directory of your choosing. For security reasons,
this should `not` be a location under your server's document root. In the rest
of this document, we will refer to this directory as `{Equation-Scorer-Root}`


Configure Apache
++++++++++++++++

All of the remaining configuration is done in the main Apache configuration file,
:file:`httpd.conf`  On my machine, this file is located at
:file:`C:\\Program Files\\Apache24\\conf\\httpd.conf`. Open this file in your favorite
text editor.

First, we need to enable the :program:`mod_wsgi`.  Locate the section that
has a whole bunch of lines that begin ``LoadModule``, and add the following::

    # MODULE mod_wsgi ADDED XX/XX/20XX
    LoadModule wsgi_module modules/mod_wsgi.so

This line enables the link between Apache and Python, but Apache still doesn't
know what Python code to invoke when it sees a particular HTTP request. To
enable that, add the following lines at the end of :file:`httpd.conf`\ ::

    # Configuration for equation scorer app
    WSGIPythonHome C:/Python27
    WSGIPythonPath {Equation-Scorer-Root}/eqscorer_rest;{Equation-Scorer-Root}/lib
    WSGIScriptAlias /eq-scorer-rest {Equation-Scorer-Root}/eqscorer_rest/eqscorer_rest/wsgi.py

Where you replace `{Equation-Scorer-Root}`, everywhere it appears, with the actual
directory to which you unzipped the AIR Equation Scoring Engine. If your Python is
not installed in the standard location, you will have to change :samp:`WSGIPythonHome`
as well.

Although Apache now knows how to run the engine, it will refuse to do so unless
you tell it that it is allowed to.  To do that, add the following
lines to the end of :file:`httpd.conf`\ ::

    <Directory "{Equation-Scorer-Root}/eqscorer_rest/eqscorer_rest">
        <Files "wsgi.py">
          Order allow,deny
          Allow from all
          Require all granted
        </Files>
    </Directory>

Again, replacing `{Equation-Scorer-Root}` with the correct value.

Now, from the Windows :guilabel:`Services` control panel, restart the Apache service. If Apache
fails to start, then chances are you mistyped something in the :file:`httpd.conf`

To test the service, fire up Fiddler, and find the :guilabel:`Composer` window. Select **POST**
for the request method. For the address, use ``http://127.0.0.1/eq-scorer-rest/isequivalent``,
for the request headers, you should specify::

    Content-Type: application/json; charset=utf-8
    Accept: application/json
    
And for the request body, you should use::

    {
      "answer":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>",
      "rubric":"<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mn>1</mn><mi>x</mi><mo>≤</mo><mn>3</mn></math>",
      "parameters":{}
    }

Push the :guilabel:`Execute` button to submit the request. After a short delay (while Python
starts and loads all of its libraries), you should get a response of ``200 OK``.  If you switch
to Fiddler's :guilabel:`Inspectors` tab, you should see something like this::

    HTTP/1.1 200 OK
    Date: Fri, 14 Jun 2013 16:38:55 GMT
    Server: Apache/2.4.4 (Win64) mod_wsgi/3.5-BRANCH Python/2.7.4
    Vary: Accept,Cookie
    Allow: POST, OPTIONS
    Transfer-Encoding: chunked
    Content-Type: application/json; charset=utf-8

    1f
    {"correct": true, "reason": ""}
    0

Now read the :doc:`API Documentation <rest_api>`, and have fun!