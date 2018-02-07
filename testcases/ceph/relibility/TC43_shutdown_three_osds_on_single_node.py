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
3. shutdown osd.0
4. shutdown osd.1
5. shutdown osd.2
5. start osd.0 
6. start osd.1
7. start osd.2
8. check the cluster status
'''

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    #client = clusterObj.getClients()[0]
    #stop osd process and start with ceph-osd -i
    clusterObj.initOsdProcess(caseName)
    
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
            
    sleep(60)
    for nodeObj in nodeList:
        osdObjList = nodeObj.getOsds()
        #out the osd
        logging.getLogger(caseName).info("\nNow operate "+nodeObj.gethostName())
        #stop osd service
        #logging.getLogger(caseName).info("Set the "+osdObj.getid()+" pid for kill")
        nodeObj.setOsdPid(caseName)
        logging.getLogger(caseName).info("shutdown two osds on node "+nodeObj.gethostName())

        osdObjList[0].shutdown(caseName, nodeObj)
        osdObjList[1].shutdown(caseName, nodeObj)
        osdObjList[2].shutdown(caseName, nodeObj)
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        #start osd service
        logging.getLogger(caseName).info("start osd on node "+nodeObj.gethostName())
        osdObjList[0].start(caseName, nodeObj)
        osdObjList[1].start(caseName, nodeObj)
        osdObjList[2].start(caseName, nodeObj)
        returnCode = osdObjList[0].checkIfOsdStart(caseName, nodeObj)
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = osdObjList[0].checkIfOsdStart(caseName, nodeObj)
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot starte"%osdObjList[0].getid())
            
        returnCode = osdObjList[1].checkIfOsdStart(caseName, nodeObj)        
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = osdObjList[1].checkIfOsdStart(caseName, nodeObj)
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot starte"%osdObjList[1].getid())
        
        returnCode = osdObjList[2].checkIfOsdStart(caseName, nodeObj)        
        tryCount = 0
        while(returnCode == 0 and tryCount < 10):
            returnCode = osdObjList[2].checkIfOsdStart(caseName, nodeObj)
            tryCount = tryCount+1
        if (tryCount == 10):
            logging.getLogger(caseName).error("%s cannot starte"%osdObjList[2].getid())
        #check ceph health
        sleep(30)
        for client in clusterObj.getClients():
            client.checkIOError(caseName)
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("stop three osds in cluster successfully")
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("kill in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)
    '''
    logging.getLogger(caseName).info("\nstop IO from clients") 
    #sleep(60)   
    for client in clusterObj.getClients():         
        base.stopIO(caseName, client)  
    '''
    for client in clusterObj.getClients():
        client.checkIOError(caseName) 
    logging.getLogger(caseName).info("%s runs complete"%caseName)      
    