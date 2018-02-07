import os, inspect
from time import sleep
from time import ctime,sleep
import base
import logs
import logging
import sys
global caseName
import paramiko
from lib.ceph import utils
from testcases.ceph.relibility.glovar import *

caseDescription = '''
start rbd IO to osd
'''
def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    for client in clusterObj.getClients():
         base.startRBDIO(caseName, client, imageNum, poolName)