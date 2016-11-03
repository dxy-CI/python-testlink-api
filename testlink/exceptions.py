#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Kai Borowiak
@summary: Exceptions for Testlink API
"""

class NotSupported(Exception):
    """To be raised, if Testlink does not support the requested method
    @cvar errorName: Method, that is not supported
    @type errorName: str
    @cvar errorCode: Default xmlrpclib.Fault code -32601
    @type errorCode: int
    """
    error_code = -32601
    def __init__(self, fn_name):
        """Initializes the Exception
        @param fn_name: Name of function causing the error
        @type fn_name: str
        """
        Exception.__init__(self, fn_name)
        self.error_msg = fn_name


class APIError(Exception):
    """To be raised, if the Testlink API returns an error struct
    @note: Default error struct {'code':'123','message':'foo'}
    @ivar errorCode: Testlink API Error Code
    @type errorCode: int
    @ivar errorString: Testlink API Error String
    @type errorString: str
    """
    def __init__(self, code='-1', message=''):
        """Initializes the Exception
        @param code: Testlink API Error Code
        @type code: int
        @param message: Testlink API Error String
        @type message: str
        """
        msg = unicode(message).encode("utf-8")
        Exception.__init__(self, str(msg))
        if not str(code).isdigit():
            code = -1
        self.error_code = int(code)
        self.error_msg = str(msg)

    def __str__(self):
        return "%d - %s" % (self.error_code, self.error_msg)


class ConnectionError(Exception):
    """To be raised, if the connection to the
    XML-RPC server cannot be stablished"""
    pass
