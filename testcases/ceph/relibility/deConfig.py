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

poolName = 'reliablityTestPool'
imageBaseName = 'reliablityTestImage'

imageNum = 10

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    clusterObj = base.getClusterObj(caseName, args)

    for i in range(0, imageNum):
        imageName = imageBaseName + str(i)        
        clusterObj.removeImg(caseName, poolName, imageName)
    clusterObj.removePool(caseName, poolName)
    logging.getLogger(caseName).info('Deconfig complete')   