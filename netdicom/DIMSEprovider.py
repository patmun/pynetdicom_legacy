#
# Copyright (c) 2012 Patrice Munger
# This file is part of pynetdicom, released under a modified MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pynetdicom.googlecode.com
#

import DIMSEmessages
import DIMSEparameters
from DIMSEmessages import DIMSEMessage
from DULparameters import P_DATA_ServiceParameters
import time
try: from queue import Empty
except ImportError: from Queue import Empty
import logging
logger = logging.getLogger(__name__)


class DIMSEServiceProvider(object):

    def __init__(self, DUL):
        self.DUL = DUL
        self.message = None

    def Send(self, primitive, id, maxpdulength):
        # take a DIMSE primitive, convert it to one or more DUL primitive and
        # send it
        if primitive.__class__ == DIMSEparameters.C_ECHO_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_ECHO_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_ECHO_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_STORE_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_STORE_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_STORE_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_FIND_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_FIND_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_FIND_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_GET_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_GET_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_GET_RSP_Message()
        if primitive.__class__ == DIMSEparameters.C_MOVE_ServiceParameters:
            if primitive.MessageID is not None:
                dimse_msg = DIMSEmessages.C_MOVE_RQ_Message()
            else:
                dimse_msg = DIMSEmessages.C_MOVE_RSP_Message()
        logger.debug('DIMSE message of class %s' % dimse_msg.__class__)
        dimse_msg.FromParams(primitive)
        logger.debug('DIMSE message: %s', str(dimse_msg))
        pdatas = dimse_msg.Encode(id, maxpdulength)
        logger.debug('encoded %d fragments' % len(pdatas))
        for ii, pp in enumerate(pdatas):
            logger.debug('sending pdata %d of %d' % (ii + 1, len(pdatas)))
            self.DUL.Send(pp)
        logger.debug('DIMSE message sent')

    def Receive(self, Wait=False, Timeout=120):
        logger.debug("In DIMSEprovider.Receive")
        if self.message is None:
            self.message = DIMSEMessage()
        if Wait:
            # loop until complete DIMSE message is received
            logger.debug('Entering loop for receiving DIMSE message')

            # If connection fails, the peek loop can iterate forever, as the
            # DUL Receive never happens. Approximate a timeout to abort
            itrs = 0
            delay = 0.001
            while 1:
                time.sleep(delay)
                nxt = self.DUL.Peek()
                if nxt is None:
                    itrs +=1
                    if Timeout and itrs > Timeout/float(delay):
                        # just like the DUL.Receive would on timeout
                        raise Empty('Timeout waiting for DIMSE message')
                    else:
                        continue

                if nxt.__class__ is not P_DATA_ServiceParameters:
                    return None, None
                if self.message.Decode(self.DUL.Receive(Wait, Timeout)):
                    tmp = self.message
                    self.message = None
                    logger.debug('Decoded DIMSE message: %s', str(tmp))
                    return tmp.ToParams(), tmp.ID
        else:
            cls = self.DUL.Peek().__class__
            if cls not in (type(None), P_DATA_ServiceParameters):
                logger.debug('Waiting for P-DATA but received %s', cls)
                return None, None
            if self.message.Decode(self.DUL.Receive(Wait, Timeout)):
                tmp = self.message
                self.message = None
                logger.debug('Received DIMSE message: %s', tmp)
                return tmp.ToParams(), tmp.ID
            else:
                return None, None
