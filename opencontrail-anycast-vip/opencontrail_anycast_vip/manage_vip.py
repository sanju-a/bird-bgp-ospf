#
# Copyright (c) 2015 Juniper Networks, Inc.
#
# author: Sanju Abraham

import argparse
import ConfigParser
import distutils.spawn
import json
import logging
import os
import requests
import sys
import time
import threading
import functools
import signal

from lb_health import LBHealth
from shell import Shell

PIDFILE="/var/run/opencontrail-anycast-vip/opencontrail-anycast-vip.pid"
timer = 0

class PeriodicTimer(object):
    def __init__(self, interval, callback):
        self.interval = interval

        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if result:
                time.sleep(self.interval)
                self.thread = threading.Thread(target=self.callback)
                try:
                   self.thread.start()
                except (KeyboardInterrupt, SystemExit):
                   self.thread.cancel()

        self.callback = wrapper

    def start(self):
        time.sleep(self.interval)
        self.thread = threading.Thread(target=self.callback)
        try:
           self.thread.start()
        except (KeyboardInterrupt, SystemExit):
           self.thread.cancel()

    def cancel(self):
        try:
           self.thread.cancel()
        except Exception as ex:
           logging.error("cancelled the execution")
        sys.exit(0)

    def join(self):
        self.thread.join()

def initialize(vip,lb_backend):
    """ Ensure that the following tools are available on the PATH """
    executables = ['haproxy', 'socat']
    for prog in executables:
        if distutils.spawn.find_executable(prog) is None:
            logging.error('%s not in PATH' % prog)
            sys.exit(1)
   
    pid=os.getpid()
    pidfile=open(PIDFILE,'w')
    pidfile.seek(0)
    pidfile.write(str(pid))
    lbh=LBHealth()
    lbh.vip=vip
    lbh.lb_backend=lb_backend
    global timer
    timer = PeriodicTimer(10, lbh.status)
    timer.start()
    timer.join()

def parse_args(args_str):
    '''
    Eg. python manage_vip.py --vip 192.168.1.17 --lb_backend contrail-api
    '''
    # Source any specified config/ini file
    # Turn off help, so we      all options in response to -h
    conf_parser = argparse.ArgumentParser(add_help=False)

    conf_parser.add_argument("-c", "--conf_file", action='append',
                             help="Specify config file", metavar="FILE")
    args, remaining_argv = conf_parser.parse_known_args(args_str.split())
    defaults = {
        'vip': '7.7.7.7',
        'lb_backend':'contrail-api',
    }

    if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read(args.conf_file)
        defaults.update(dict(config.items("DEFAULTS")))

    # Override with CLI options
    # Don't surpress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        # print script description with -h/--help
        description=__doc__,
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(**defaults)
    parser.add_argument("--vip", help="VIP address for the contrail cluster")
    parser.add_argument("--lb_backend", help="LB backend to check for connectivity")
    args = parser.parse_args(remaining_argv)
    return args

def signal_handler(signal, frame):
        timer.cancel()
        sys.exit(0)

def main(args_str=None):
    if os.path.isfile(PIDFILE):
       os.remove(PIDFILE)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='/var/log/vip_manage.log',
                        level=logging.DEBUG)
    logging.debug(' '.join(sys.argv))
    if not args_str:
        args_str = ' '.join(sys.argv[1:])
    args = parse_args(args_str)
    initialize(args.vip, args.lb_backend)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
