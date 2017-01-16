#
# Copyright (c) 2012 Patrice Munger
# This file is part of pynetdicom, released under a modified MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pynetdicom.googlecode.com
#

# Timer class
import time
import logging

import threading

logger = logging.getLogger(__name__)


class Timer:

    def __init__(self, MaxNbSeconds):
        self.__MaxNbSeconds = MaxNbSeconds
        self.__StartTime = None

        # Re-entrant lock required as Restart is sometimes called during Check
        # which means __StartTime can unexpectedly become None
        self.__Lock = threading.RLock()

    def Start(self):
        logger.debug("Timer started")

        with self.__Lock:
            self.__StartTime = time.time()

    def Stop(self):
        logger.debug("Timer stopped")
        with self.__Lock:
            self.__StartTime = None

    def Restart(self):
        with self.__Lock:
            if self.__StartTime is not None:
                self.Stop()
                self.Start()
            else:
                self.Start()

    def Check(self):
        with self.__Lock:
            if self.__StartTime:
                if time.time() - self.__StartTime > self.__MaxNbSeconds:
                    logger.warning("Timer expired")
                    return False
                else:
                    return True
            else:
                return True


if __name__ == '__main__':

    t = Timer(3)

    t.Start()
    for ii in range(32):
        time.sleep(0.2)
        print t.Check()
