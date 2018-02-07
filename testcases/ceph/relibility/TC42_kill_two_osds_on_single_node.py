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
3. random pick two osds and kill them
4. start the killed osds
5. check the cluster status
6. repeat step 2-5 on the other node
'''

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    client = clusterObj.getClients()[0]
    #stop osd process and start with ceph-osd -i
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
    logging.getLogger(caseName).info("\nStep2:start force kill osd")
    for nodeObj in nodeList:    
        osdObjList = nodeObj.getOsds()
        #out the osd
        logging.getLogger(caseName).info("\nNow operate "+nodeObj.gethostName())
        #stop osd service
        #logging.getLogger(caseName).info("Set the "+osdObj.getid()+" pid for kill")
        nodeObj.setOsdPid(caseName)
        logging.getLogger(caseName).info("shutdown two osds on node "+nodeObj.gethostName())
        firOsdId = random.randint(0, len(osdObjList)-1)
        secOsdId = random.randint(0, len(osdObjList)-1)
        while ( firOsdId == secOsdId):
            secOsdId = random.randint(0, len(osdObjList)-1)
        osdObjList[firOsdId].forceKill(caseName, nodeObj)
        osdObjList[secOsdId].forceKill(caseName, nodeObj)
        sleep(60)
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        #start osd service
        logging.getLogger(caseName).info("start osd on node "+nodeObj.gethostName())
        osdObjList[firOsdId].start(caseName, nodeObj)
        osdObjList[secOsdId].start(caseName, nodeObj)
        returnCode = osdObjList[firOsdId].checkIfOsdStart(caseName, nodeObj)
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = osdObjList[firOsdId].checkIfOsdStart(caseName, nodeObj)
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot start"%osdObjList[firOsdId].getid())
        returnCode = osdObjList[secOsdId].checkIfOsdStart(caseName, nodeObj)
        
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = osdObjList[secOsdId].checkIfOsdStart(caseName, nodeObj)
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot start"%osdObjList[secOsdId].getid())

        #check ceph health
        sleep(30)
        for client in clusterObj.getClients():         
            client.checkIOProcess(caseName ) 
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("kill two osds in cluster successfully")
            for client in clusterObj.getClients():         
                client.checkIOProcess(caseName) 
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("kill in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)
    '''
    logging.getLogger(caseName).info("\nStep3: stop IO from clients") 
    #sleep(60)   
    for client in clusterObj.getClients():         
        base.stopIO(caseName, client)  
    '''
    for client in clusterObj.getClients():
        client.checkIOError(caseName) 
    logging.getLogger(caseName).info("%s runs complete"%caseName)      
    