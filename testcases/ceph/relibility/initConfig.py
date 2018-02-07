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

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    #init process
    logging.getLogger(caseName).info('Init osd process') 
    #clusterObj.initOsdProcess(caseName)
    
    clusterObj.createPool(caseName, poolName, pgNumber)
    poolObj = clusterObj.getPoolByname(caseName, poolName)
    
    #############Image operation
    #print poolObj.pgNumber
    imageSize = baseSize
    for client in clusterObj.getClients():
        if(IOMode == 'rbd'):
            imageBaseName  = client.gethostName() + 'rbdImg'
            for i in range(0, imageNum):
                print imageSize
                imageName = imageBaseName + str(i)        
                clusterObj.createImg(caseName,size = imageSize, pool = poolName, imageName = imageName)
                imageSize = utils.add(imageSize, increment)
        elif(IOMode == 'nbd'):
            for i in range(0, imageNum):
                if(i<imageNum/2):
                    imageBaseName  = client.gethostName() + 'nbdBlockImg'
                    imageName = imageBaseName + str(i)
                else:
                    imageBaseName  = client.gethostName() + 'nbdFileImg'
                    imageName = imageBaseName + str(i-imageNum/2)        
                clusterObj.createImg(caseName,size = imageSize, pool = poolName, imageName = imageName)
                imageSize = utils.add(imageSize, increment)
        
    logging.getLogger(caseName).info('Init config complete')   