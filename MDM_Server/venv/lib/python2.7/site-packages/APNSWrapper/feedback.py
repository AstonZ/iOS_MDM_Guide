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

import datetime
import sys
import struct

from connection import *

class APNSFeedbackWrapper(object):
    """
    This object wrap Apple Push Notification Feedback Service tuples.
    Object support for iterations and may work with routine cycles like for.
    """
    sandbox = True
    apnsHost = 'feedback.push.apple.com'
    apnsSandboxHost = 'feedback.sandbox.push.apple.com'
    apnsPort = 2196
    feedbacks = None
    connection = None
    testingParser = False

    blockSize = 1024 # default size of SSL reply block is 1Kb
    feedbackHeaderSize = 6

    enlargeRecursionLimit = lambda self: sys.setrecursionlimit(sys.getrecursionlimit() + 100)

    _currentTuple = 0
    _tuplesCount = 0

    def __init__(self, certificate = None, sandbox = True, force_ssl_command = False, debug_ssl = False):
        self.debug_ssl = debug_ssl
        self.force_ssl_command = False
        self.connection = APNSConnection(certificate = certificate, \
                            force_ssl_command = self.force_ssl_command, debug = self.debug_ssl)

        self.sandbox = sandbox
        self.feedbacks = []
        self._currentTuple = 0
        self._tuplesCount = 0

    def __iter__(self):
        return self

    def next(self):
        if self._currentTuple >= self._tuplesCount:
            raise StopIteration

        obj = self.feedbacks[self._currentTuple]
        self._currentTuple += 1
        return obj

    def _parse_reply(self, reply):
        flag = True
        offset = 0
        while(flag):
            try:
                feedbackTime, tokenLength = struct.unpack_from('!lh', reply, offset)
                deviceToken = struct.unpack_from('%ds' % tokenLength, reply, offset + 6)[0]
                offset += 6 + len(deviceToken)

                self._append(feedbackTime, deviceToken)
            except:
                flag = False

    def tuples(self):
        """
        This method return a list with all received deviceTokens:
        ( datetime, deviceToken )
        """
        return self.feedbacks

    def _append(self, fTime, token):
        self.feedbacks.append((datetime.datetime.fromtimestamp(fTime), token))
        self._tuplesCount = len(self.feedbacks)

    def _parseHeader(self, Buff):
        """
        Parse header of Feedback Service tuple.
        Format of Buff is |xxxx|yy|zzzzzzzz|
            where:
                x is time_t (UNIXTIME, long, 4 bytes)
                y is length of z (two bytes)
                z is device token
        """
        try:
            feedbackTime, tokenLength = struct.unpack_from('!lh', Buff, 0)
            if Buff >= self.feedbackHeaderSize + tokenLength:
                recoursiveInvoke = lambda: self._parseTuple(feedbackTime, tokenLength, Buff[self.feedbackHeaderSize:])

                # enlarge recursion limit if it is exceeded
                try:
                    return recoursiveInvoke()
                except RuntimeError:
                    self.enlargeRecursionLimit()
                    return recoursiveInvoke()
            else:
                return Buff
        except:
            return Buff

    def _parseTuple(self, tTime, tLen, Buff):
        """
        Get body by length tLen of current Feedback Service tuple.
        If body length is equal to tLen than append new
        tuple item and recoursive parse next item.

        """
        try:
            token = struct.unpack_from('!%ds' % tLen, Buff, 0)[0]
            self._append(tTime, token)
        except:
            pass

        recurrenceInvoke = lambda: self._parseHeader(Buff[tLen:])
        # enlarge recursion limit if it is exceeded
        try:
            return recurrenceInvoke()
        except RuntimeError:
            self.enlargeRecursionLimit()
            return recurrenceInvoke()

    def _testFeedbackFile(self):
        fh = open('feedbackSampleTuple.dat', 'r')
        return fh

    def receive(self):
        """
        Receive Feedback tuples from APNS:
            1) make connection to APNS server and receive
            2) unpack feedback tuples to arrays
        """

        apnsConnection = self.connection

        if self.sandbox != True:
            apnsHost = self.apnsHost
        else:
            apnsHost = self.apnsSandboxHost

        apnsConnection.connect(apnsHost, self.apnsPort)

        tRest = None
        blockSize = self.blockSize

        # replace connectionContext to similar I/O function but work
        # with binary Feedback Service sample file
        if self.testingParser:
            connectionContext = self._testFeedbackFile()

        replyBlock = apnsConnection.read(blockSize)

        while replyBlock:
            if tRest and len(tRest) > 0:
                # merge previous rest of replyBlock and new
                replyBlock = struct.pack('!%ds%ds' % (len(tRest), len(replyBlock)), tRest, replyBlock)
            tRest = self._parseHeader(replyBlock)
            replyBlock = apnsConnection.read(blockSize)

        # close sample binary file
        if self.testingParser:
            connectionContext.close()

        apnsConnection.close()
        return True
