#
# Copyright (c) 2015 Juniper Networks, Inc.
#
# author: Sanju Abraham

import logging
import os
import re
from shell import Shell

class VipIntfManager(object):
    def __init__(self):
        pass

    def create_interface(self, vip):
        try:
            vip=vip.split("/",1)[0]
            Shell.run('ifconfig lo:1 %s netmask 255.255.255.255 up' % (vip))
            logging.debug("Assigned VIP to the loopback interface")
        except Exception as ex:
              logging.error(ex)

    def clear_interface(self, vip):
        try:
           vip=vip.split("/",1)[0]
           Shell.run('ifconfig lo:1 %s netmask 255.255.255.255 down' % (vip))
           logging.debug("Removed VIP from loopback interface due to all backend failures")
        except Exception as ex:
               logging.error(ex)
