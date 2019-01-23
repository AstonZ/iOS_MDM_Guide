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


import os
import socket
import subprocess

from apnsexceptions import *
from utils import *

class APNSConnectionContext(object):
    certificate = None
    def __init__(self, certificate = None):
        self.certificate = certificate
    def connect(self, host, port):
        raise APNSNotImplementedMethod, "APNSConnectionContext.connect ssl method not implemented in context"
    def write(data = None):
        raise APNSNotImplementedMethod, "APNSConnectionContext.write method not implemented"
    def read(self):
        raise APNSNotImplementedMethod, "APNSConnectionContext.read method not implemented"
    def close(self):
        raise APNSNotImplementedMethod, "APNSConnectionContext.close method not implemented"



class OpenSSLCommandLine(APNSConnectionContext):
    """
    This class execute and send data with openssl command line tool
    """

    certificate = None
    host = None
    port = None
    executable = None
    debug = False
    def __init__(self, certificate = None, executable = None, debug = False):
        self.certificate = certificate
        self.executable = executable
        self.debug = debug

    def connect(self, host, port):
        self.host = host
        self.port = port

    def _command(self):
        command = "%(executable)s s_client -ssl3 -cert %(cert)s -connect %(host)s:%(port)s" % \
            {
            'executable' : self.executable,
            'cert' : self.certificate,
            'host' : self.host,
            'port' : self.port
            }

        return subprocess.Popen(command.split(' '), shell=False, bufsize=256, \
            stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    def write(self, data = None):
        pipe = self._command()

        std_in = pipe.stdin
        std_in.write(data)
        std_in.flush()
        std_in.close()

        std_out = pipe.stdout
        if self.debug:
            print "-------------- SSL Debug Output --------------"
            print command
            print "----------------------------------------------"
            print std_out.read()
            std_out.close()
        pipe.wait()

    def read(self, blockSize = 1024):
        """
        There is method to read data from feedback service.
        WARNING! It's not tested and doesn't work yet!
        """
        pipe = self._command()
        std_out = pipe.stdout

        data = std_out.read()

        #pipe.wait()
        std_out.close()
        return data


    def context(self):
        return self

    def close(self):
        pass

class SSLModuleConnection(APNSConnectionContext):
    """
    This is class which implement APNS connection based on
    "ssl" module.
    """

    socket = None
    certificate = None
    connectionContext = None
    ssl_module = None

    def __init__(self, certificate = None, ssl_module = None):
        self.socket = None
        self.connectionContext = None
        self.certificate = certificate
        self.ssl_module = ssl_module

    def context(self):
        """
        Initialize SSL context.
        """
        if self.connectionContext != None:
            return self

        self.socket = socket.socket()
        self.connectionContext = self.ssl_module.wrap_socket(
                    self.socket,
                    ssl_version = self.ssl_module.PROTOCOL_SSLv3,
                    certfile = self.certificate
                )

        return self


    def certificate(self, path):
        self.certificate = path
        return self

    def read(self, blockSize = 1024):
        """
        Make connection to the host and port.
        """

        return self.connectionContext.read(blockSize)

    def write(self, data = None):
        """
        Make connection to the host and port.
        """

        self.connectionContext.write(data)

    def connect(self, host, port):
        """
        Make connection to the host and port.
        """

        self.connectionContext.connect((host, port))

    def close(self):
        """
        Close connection.
        """
        self.connectionContext.close()
        self.socket.close()


class APNSConnection(APNSConnectionContext):
    """
    APNSConnection wrap SSL connection to the Apple Push Notification Server.
    """

    debug = False
    connectionContext = None

    def __init__(self, certificate = None,
                        ssl_command = "openssl",
                        force_ssl_command = False,
                        disable_executable_search = False,
                        debug = False):
        self.connectionContext = None
        self.debug = debug

        if not os.path.exists(str(certificate)):
            raise APNSCertificateNotFoundError, "Apple Push Notification Service Certificate file %s not found." % str(certificate)

        try:
            if force_ssl_command:
                raise ImportError, "There is force_ssl_command forces command line tool"

            # use ssl library to handle secure connection
            import ssl as ssl_module
            self.connectionContext = SSLModuleConnection(certificate, ssl_module = ssl_module)
        except:
            # use command line openssl tool to handle secure connection
            if not disable_executable_search:
                executable = find_executable(ssl_command)
            else:
                executable = ssl_command

            if not executable:
                raise APNSNoCommandFound, "SSL Executable [%s] not found in your PATH environment" % str(ssl_command)

            self.connectionContext = OpenSSLCommandLine(certificate, executable, debug = debug)

        self.certificate = str(certificate)

    def connect(self, host, port):
        """
        Make connection to the host and port.
        """
        self.context().connect(host, port)
        return self

    def certificate(self, path):
        self.context().certificate(path)
        return self

    def write(self, data = None):
        self.context().write(data)

    def read(self, blockSize = 1024):
        return self.context().read(blockSize)

    def context(self):
        if not self.connectionContext:
            raise APNSNoSSLContextFound, "There is no SSL context available in your python environment."
        return self.connectionContext.context()

    def close(self):
        """
        Close connection.
        """
        self.context().close()
