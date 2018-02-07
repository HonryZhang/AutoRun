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
This test case will do the following steps:
1. start IO on 10 images with randwrite and verify
2. login the first node 
3. remove one osd from the first node
4. login the second node
5. remove one osd from the second node
'''

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    #client = clusterObj.getClients()[0]
    
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, clusterObj.getFirstAvaNode(caseName), timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
        
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)     
    #upload script
    nodeList[0].uploadScript(caseName)
    nodeList[1].uploadScript(caseName)

    logging.getLogger(caseName).info("\nStep2: kill one osd from two node")
    for i in range(10):
        logging.getLogger(caseName).info("start to delete osd on node %s "%nodeList[0].gethostName())
        nodeList[0].setOsdDisk(caseName)
        diskDict = {}
        osdObjs = nodeList[0].getOsds()
        #for remove with delete script
        osdObjs[0].forceKill(caseName, nodeList[0])
        osdObjs[0].userStart(caseName, nodeList[0])
        
        diskDict[nodeList[0].gethostName()] = osdObjs[0].getDisk()
        osdObjs[0].delete(caseName, nodeList[0])
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeList[0], timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("%s create succesfully"%osdObjs[0].getid())
        logging.getLogger(caseName).info("osd was delete successfully on node %s "%nodeList[0].gethostName())
        clusterObj.updateCluster(nodeList[0])
        
        logging.getLogger(caseName).info("start to delete osd on node %s "%nodeList[1].gethostName())
        nodeList[1].setOsdDisk(caseName)
        osdObjs2 = nodeList[1].getOsds()
        logging.getLogger(caseName).info(osdObjs2)
        #for remove with delete script
        osdObjs2[0].forceKill(caseName, nodeList[1])
        osdObjs2[0].userStart(caseName, nodeList[1])
        diskDict[nodeList[1].gethostName()] = osdObjs2[0].getDisk()
        osdObjs2[0].delete(caseName, nodeList[1])
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeList[1], timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("%s delete succesfully"%osdObjs2[0].getid())
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            status = clusterObj.getStatus(caseName, nodeList[1], timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("stop in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)  
        logging.getLogger(caseName).info("osd was delete successfully on node %s "%nodeList[1].gethostName())
        clusterObj.updateCluster(nodeList[1])
        
       # for disk in diskDict.values():
        disk0 = diskDict[nodeList[0].gethostName()]
        disk1 = diskDict[nodeList[1].gethostName()]
        logging.getLogger(caseName).info("start to create osd on %s"%nodeList[0].gethostName()) 
        nodeList[0].createOsd(caseName,disk0)
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeList[0], timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("osd on %s create succesfully"%nodeList[0].gethostName())
        clusterObj.updateCluster(nodeList[0])
            
        logging.getLogger(caseName).info("start to create osd on %s"%nodeList[1].gethostName()) 
        nodeList[1].createOsd(caseName,disk1)
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeList[1], timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("osd on %s create succesfully"%nodeList[1].gethostName())
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            status = clusterObj.getStatus(caseName, nodeList[1], timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("stop in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)    
        clusterObj.updateCluster(nodeList[1])    

        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        for client in clusterObj.getClients():         
            if(client.checkIOProcess(caseName ) == "error"):
                base.startRBDIO(caseName, client, imageNum, poolName)
    logging.getLogger(caseName).info("case runs complete")
    return 1
    
    