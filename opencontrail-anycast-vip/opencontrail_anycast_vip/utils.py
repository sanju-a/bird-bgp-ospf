import os
import logging
import subprocess
import re
from shell import Shell

class Utils:
     @staticmethod
     def findProcess( process_name ):
         ps = subprocess.Popen("ps -A | grep "+process_name, shell=True, stdout=subprocess.PIPE)
         output = ps.stdout.read()
         ps.stdout.close()
         ps.wait()
         return output

     @staticmethod
     def isRunning( process_name ):
          output = Utils.findProcess( process_name )
          if re.search(process_name, output) is None:
             return False
          else:
             return True

     @staticmethod
     def isVIPPresent(intf):
         f = os.popen('ifconfig lo:1 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
         vip=f.read()
         if vip:
            return True
         else: 
            return False

     @staticmethod
     def isBackendDown(backend):
         socatstr='echo "show stat -1 2 -1" | socat unix-connect:/var/run/haproxy.sock stdio | grep %s | grep -o DOWN' % backend
         f = os.popen('%s' % socatstr)
         bkend=f.read()
         if bkend:
            return True
         else:
            return False
