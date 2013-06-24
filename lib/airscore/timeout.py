#################################################################################
# Equation Scoring Engine
# Copyright (c) 2013 American Institutes for Research
# 
# Distributed under the AIR Open Source License, Version 1.0
# See accompanying file AIR-License-1_0.txt or at 
# https://bitbucket.org/sbacoss/equationscorer/wiki/AIR_Open_Source_License_1.0
#################################################################################

import ctypes
import time
import threading
import traceback
import logging
import sys


"""Code to throw a TimeoutError "at" a thread if it takes too long to execute
"""

MAX_TIMEOUT = 60
SLEEP_INTERVAL = 1.0
RESCHEDULE_INTERVAL = 5

_BUFFER_SIZE = MAX_TIMEOUT + 1
_CIRCLE_BUFFER = [ set() for i in xrange( _BUFFER_SIZE ) ]
_I = 0
_LOCK = threading.RLock()
_TIMING_THREADS = set()
_LOGGER = logging.getLogger( 'airscore.timeout' )

class Timeout( object ):
    """A context manager to enforce a timeout
    
    Example::

        with Timeout( 3 ):
            myfun( blah )
    
    will cause myfun to raise a TimeoutError after three seconds if the underlying function
    has not yet returned.
    
    CAVEATS
    
        + The error will not be raised if ``myfun()`` is blocked in non-Python code.
        
        + The timing will be imprecise
        
        + A maximum timeout of 60 seconds is currently supported
        
        + Timeout objects are _not_ reentrant.
        
    """
    def __init__( self, t ):
        if not isinstance( t, int ) or t < 1 or t > MAX_TIMEOUT:
            raise ValueError( "Timeout must be an integer number of seconds between 1 and {}".format( MAX_TIMEOUT) )
        self.t = t
        
    
    def __enter__( self ):
        with _LOCK:
            thread = threading.current_thread()
            if thread in _TIMING_THREADS:
                raise RuntimeError( "Cannot nest Timeout managers in a single thread" )
            _TIMING_THREADS.add( thread )
            i = ( _I + self.t ) % _BUFFER_SIZE
            _CIRCLE_BUFFER[ i ].add( thread )
            self.timeout_thread = thread
            self.index = i
        
    def __exit__( self, exc_type, exc_val, exc_tb ):
        with _LOCK:
            thread = self.timeout_thread
            buffer_cell = _CIRCLE_BUFFER[ self.index ]
            if thread in _TIMING_THREADS:
                _TIMING_THREADS.remove( thread )
            if thread in buffer_cell:
                buffer_cell.remove( thread )

class TimeoutError( BaseException ):
    pass

class Watchdog( threading.Thread ):
    
    def __init__(self):
        super( Watchdog, self ).__init__()
        self.daemon = True
        self.event = threading.Event()
        
    def run(self):
        global _I
        try:
            while True:
                with _LOCK:
                    i_reschedule = ( _I + RESCHEDULE_INTERVAL ) % _BUFFER_SIZE
                    for thread in _CIRCLE_BUFFER[ _I ]:
                        # C API call: returns zero on failure
                        res = ctypes.pythonapi.PyThreadState_SetAsyncExc( thread.ident, ctypes.py_object( TimeoutError ) )
                        if thread is threading.current_thread():
                            continue
                        if res == 0:
                            ctypes.pythonapi.PyThreadState_SetAsyncExc( thread.ident, ctypes.py_object( 0 ) )
                        # Reschedule the interrupt (in case one try doesn't work)
                        _CIRCLE_BUFFER[ i_reschedule ].add( thread )
                    _CIRCLE_BUFFER[ _I ].clear()
                    _I = ( _I + 1 ) % _BUFFER_SIZE
                time.sleep( SLEEP_INTERVAL )
        except BaseException:
            _LOGGER.exception( "Watchdog thread has exited on an exception!!" )

_INTERRUPTER_THREAD = Watchdog()
_INTERRUPTER_THREAD.start()
