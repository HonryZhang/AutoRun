import os, inspect
from time import sleep
from time import ctime,sleep
import base
import logs
import logging
import sys
global caseName
import paramiko
from testcases.ceph.relibility.glovar import *
import random

caseDescription = '''
This test case will do the following steps:
1. start IO on 10 images with randwrite and verify
2. login the first node 
3. random pick one osd and stop them
4. check the cluster status
5. login the second node 
6. random pick one osd and stop them
7. check the cluster status
8. start the stopped osd from the first node
9. start the stopped osd from the second node
10. check the cluster status
'''

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    #client = clusterObj.getClients()[0]
    clusterObj.initOsdProcess(caseName)
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
            
    sleep(60)
    logging.getLogger(caseName).info("\nStep2: start kill one osd on two node 10 times")
    for i in range(10):
        logging.getLogger(caseName).info("\nThis is the %d loop"%i)
        firOsdList = nodeList[0].getOsds()
        secOsdList = nodeList[1].getOsds()
        firOsdId = random.randint(0, len(firOsdList)-1)
        secOsdId = random.randint(0, len(secOsdList)-1)
        firOsdList[firOsdId].forceKill(caseName, nodeList[0])
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeList[0], timeOut)        
        secOsdList[secOsdId].forceKill(caseName, nodeList[1])
         
        logging.getLogger(caseName).info("\nsleep 120 seconds then start the osd") 
        sleep(120)  
        firOsdList[firOsdId].start(caseName, nodeList[0])
        secOsdList[secOsdId].start(caseName, nodeList[1]) 

        returnCode = firOsdList[firOsdId].checkIfOsdStart(caseName, nodeList[0])
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = firOsdList[firOsdId].checkIfOsdStart(caseName, nodeList[0])
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot start"%firOsdList[firOsdId].getid())    
        
        returnCode = secOsdList[secOsdId].checkIfOsdStart(caseName, nodeList[1])
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = secOsdList[secOsdId].checkIfOsdStart(caseName, nodeList[1])
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot start"%secOsdList[secOsdId].getid())        
        
        logging.getLogger(caseName).info("\nAdd osd into cluster")
        firOsdList[firOsdId].inCluster(caseName, nodeList[0])
        secOsdList[secOsdId].inCluster(caseName, nodeList[1]) 
        
        #check cluster status 
        status = clusterObj.getStatus(caseName, nodeList[0], timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("Kill osd on two nodes successfully")
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            status = clusterObj.getStatus(caseName, nodeList[0], timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("kill in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)
                
        for client in clusterObj.getClients():
            client.checkIOError(caseName)  
        for client in clusterObj.getClients():         
            if(client.checkIOProcess(caseName ) == "error"):
                base.startRBDIO(caseName, client, imageNum, poolName)    
    
    logging.getLogger(caseName).info("%s runs complete"%caseName)      
    