#
# Copyright (c) 2015 Juniper Networks, Inc.
#

import logging
import os
import re
import subprocess
from shell import Shell
from vip_intf_manager import VipIntfManager
from utils import Utils

_HAP = "haproxy"

class LBHealth(object):

    def __init__(self):
        self._vip = None
        self._lb_backend = None

    @property
    def vip(self):
        # Do something if you want
        return self._vip

    @vip.setter
    def vip(self, value):
        # Do something if you want
        self._vip = value

    @property
    def lb_backend(self):
        # Do something if you want
        return self._vip

    @lb_backend.setter
    def lb_backend(self, value):
        # Do something if you want
        self._lb_backend = value

    def status(self):
        vipmgr=VipIntfManager()
        if Utils.isRunning(_HAP):
           if Utils.isBackendDown(self._lb_backend):
              logging.debug("Backends are not up")
              if Utils.isVIPPresent(self._vip):
                 # Remove VIP
                 vipmgr.clear_interface(self._vip)
           else:
              if not Utils.isBackendDown(self._lb_backend):
                 logging.debug("Assigning VIP")
                 # Assign VIP
                 vipmgr.create_interface(self._vip)
        else:
             # Remove VIP
             vipmgr.clear_interface(self._vip)
        return True
