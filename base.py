import os
import sys
import logs
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from lib.ceph import *
import logging
from testcases.ceph.relibility.glovar import *

def getClusterObj(caseName, testEnvXml):
    clusterObj = cluster(caseName,testEnvXml)
    #print clusterObj.getStatus()
    return clusterObj

#start IO from the client, imageNum IO process per client
def startIO(caseName, client, IOMode):
    #pidList= []
    if(IOMode == 'rbd'):
        #imageBaseName  = client.gethostName() + 'rbdImg'
        startRBDIO(caseName, client, imageNum, poolName)
    elif(IOMode == 'nbd'):
        #half of the image will used for filesystem, half of the image will used for block directly
        #imageBaseName = client.gethostName() + 'nbdBlockImg'
        startNBDBlockIO(caseName, client, imageNum/2, poolName)
        #imageBaseName = client.gethostName() + 'nbdFileImg'
        startNBDFileIO(caseName, client, imageNum/2, poolName)
        #pidList.append(blockPidList)
        #pidList.append(filePidList)
    #return pidList

def startRBDIO(caseName, client, imageNum, poolName):
    #pidList = []
    imageBaseName  = client.gethostName() + 'rbdImg'
    imageSize = baseSize
    for i in range(0, imageNum):
        imageName = imageBaseName + str(i) 
        logging.getLogger(caseName).info("\nNow start IO on  "+imageName)
        client.writeRbdFio(caseName, imageName, poolName, imageSize) 
        imageSize = utils.add(imageSize, increment)
       # pidList.append(pid)
    #pid = client.writeRbdFio(caseName, imageName, poolName)
    #return pidList
 
def startNBDBlockIO(caseName, client, imageNum, poolName):
    #pidList = []
    imageBaseName = client.gethostName() + 'nbdBlockImg'
    imageDiskDict = {}
    imageSize = baseSize
    for i in range(0, imageNum):
        imageName = imageBaseName + str(i) 
        logging.getLogger(caseName).info("\nNow start IO on  "+imageName)
        disk = client.mapNbd(caseName, poolName, imageName)
        imageDiskDict[imageName] = disk
        client.writeNbdBlockIO(caseName, rate, disk, imageSize) 
        imageSize = utils.add(imageSize, increment)
        #pidList.append(pid)
    #pid = client.writeRbdFio(caseName, imageName, poolName)
    #return pidList

def startNBDFileIO(caseName, client,  imageNum, poolName):
    #pidList = []
    imageDiskDict = {}
    imageBaseName = client.gethostName() + 'nbdFileImg'
    imageSize =  utils.sub(baseSize, '10G')
    for i in range(0, imageNum):
        imageName = imageBaseName + str(i) 
        logging.getLogger(caseName).info("\nNow start IO on  "+imageName)
        disk = client.mapNbd(caseName, poolName, imageName)
        imageDiskDict[imageName] = disk
        #make fs               
        client.writeNbdFileIO(caseName,disk, 'ext2', imageSize) 
        imageSize = utils.add(imageSize, increment)
        #pidList.append(pid)
    #pid = client.writeRbdFio(caseName, imageName, poolName)
    #return pidList

def stopIO(caseName,client):
    #client.stopFio(caseName, pid)    
    client.stopFio(caseName)
    