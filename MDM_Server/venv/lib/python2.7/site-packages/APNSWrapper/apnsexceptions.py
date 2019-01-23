# Copyright 2009 Max Klymyshyn, Sonettic
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



class APNSNotImplementedMethod(Exception):
    """
    This exception raised when you method of ssl context
    was not implemented. Only for testing purposes.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSNoSSLContextFound(Exception):
    """
    This exception raised when you haven't available SSL context
    in your environment
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class APNSNoCommandFound(Exception):
    """
    This exception raised when you try to find SSL executable but
    it will not be found in your PATH
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSTypeError(Exception):
    """
    This exception raised when you try to add an argument with
    unexpected type.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSPayloadLengthError(Exception):
    """
    If length of payload more than 256 (by APNS specification) generate this exception
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSCertificateNotFoundError(Exception):
    """
    This exception raised when you try to add an argument with
    certificate file but certificate not found.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSValueError(Exception):
    """
    This exception raised when you try to add value to method
    which expect concrete type of argument.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class APNSUndefinedDeviceToken(Exception):
    """
    This exception raised when you try to send notifications by wrapper
    but one of notification don't have deviceToken.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class APNSConnectionError(Exception):
    """
    This is a simple exception which generated when
    you can't connect to APNS service or your
    certificate is not valid.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
