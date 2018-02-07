import os, inspect
from time import sleep
from time import ctime,sleep
import base
import logs
import logging
import sys
global caseName
import paramiko
#from testcases.relibility.glovar import *

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    #print utils.add('10GB','10G')
    #send testenv as argument, then parse it as a object
    #TBD: change it to arguments
    #imageDiskDict = {}
    clusterObj = base.getClusterObj(caseName, args)
    '''
    for client in clusterObj.getClients(): 
        disk = client.mapNbd(caseName, 'reliablityTestPool', 'IO_test')
        logging.getLogger(caseName).info(disk)
    '''
    '''
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
    '''
    '''        
    for client in clusterObj.getClients():         
        client.checkIOProcess(caseName ) 
    
    for client in clusterObj.getClients():         
        base.stopIO(caseName, client) 
    ''' 
    #client = clusterObj.getClients()[0].checkIOError(caseName)
    #print len(clusterObj.getNodes())
    nodeList = clusterObj.getNodes()
    logging.getLogger(caseName).info("case 1 start") 
    logging.getLogger(caseName).info(len(nodeList[0].getOsds())) 
    #    osdObj = nodeObj.getOsds()[0]
    disks = []
    
    nodeList[0].setOsdDisk(caseName)
    for osdObj in nodeList[0].getOsds():
        logging.getLogger(caseName).info(osdObj.getid())
        disks.append(osdObj.getDisk()) 
    print disks
    #nodeList[0].setOsdPid(caseName)
    
    #for nodeObj in nodeList:

        #nodeObj.setOsdPid(caseName)
    
    '''
    monitors = clusterObj.getMonitors()
    monitors[0].setMonPid(caseName)
    monitors[0].shutdown(caseName)
    monitors[0].start(caseName)
    monitors[0].checkIfMonStart(caseName)
    '''
    '''
    node = clusterObj.getFirstAvaNode(caseName)
    node.uploadScript(caseName)
    '''
    #clusterObj.getStatus(caseName, nodeList[0], timeOut)
    #clusterObj.initOsdProcess(caseName)
    '''
    clients = clusterObj.getClients()
    clients[0].writeNbdFileIO(caseName,'/dev/nbd5' , 'ext2')
    '''
    '''
    for client in clients:
        base.startIO(caseName, client)
    '''
    '''    
    imageSize = baseSize
    imageDiskDict = {}
    for i in range(0, imageNum):
        print imageSize
        imageName = imageBaseName + str(i) 
        disk = clients[0].mapNbd(caseName, poolName, imageName)
        imageDiskDict[imageName] = disk
        clients[0].writeNbdBlockIO(caseName, imageSize, rate, disk)
        
    base.stopIO(caseName, clients[0])
    for i in range(0, imageNum):
        print imageSize
        imageName = imageBaseName + str(i) 
        disk = clients[0].unmapNbd(caseName, imageName, imageDiskDict[imageName])
    '''   
    #pid = clients[0].writeRbdFio(caseName, 'becky', 'becky')
    #sleep(5)
    #clients[0].stopFio(caseName, pid)
    '''
    avaiNode = clusterObj.getFirstAvaNode(caseName)
    #avaiNode.setOsdPid(caseName)
    avaiNode.setOsdDisk(caseName)
    
    osdlist = avaiNode.getOsds()
    osdlist[0].delete(caseName,avaiNode )
    #avaiNode.create(caseName, 'sdb')
    clusterObj.updateOsds(avaiNode)
    osdList = clusterObj.getOsds()
    for osdObj in osdList:
        print osdObj.getid()
    '''
    #osdlist[1].delete(caseName, avaiNode)
    #avaiNode.initOsdProcess(caseName)
    #print avaiNode.gethostName()
    #osdlist[0].kill(caseName, avaiNode)
    #osdlist[0].outCluster(caseName, avaiNode)
    #osdlist[0].shutdown(caseName, avaiNode)
    #osdlist[0].start(caseName, avaiNode)
    #osdlist[0].inCluster(caseName, avaiNode)
    #osdlist[0].inCluster(caseName, avaiNode)
    #avaiNode.initOsdProcess(caseName)
    
    
    #print osdlist
    '''
    status = clusterObj.getStatus(avaiNode)
    logging.getLogger(caseName).info(status)
    clusterObj.createPool(caseName, 'becky_Test', '20')
    poolObj = clusterObj.getPoolByname(caseName, 'becky_Test')
    '''
    
    #############Image operation
    #print poolObj.pgNumber
    #clusterObj.createImg(caseName,size = '10G', pool = 'becky_Test', imgname = 'testImg')
    #clusterObj.removePool(caseName, 'becky_Test')
    return 1
 