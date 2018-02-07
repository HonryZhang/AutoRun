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

caseDescription = '''
This test case will do the following steps:
1. start IO on 10 images with randwrite and verify
2. pause the cluster 
3. check if IO can start or not
4. resume the cluster
5. check if IO can start or not
'''


def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    clusterObj.initOsdProcess(caseName)
    #client = clusterObj.getClients()[0]
    #nodeObj = clusterObj.getFirstAvaNode(caseName)
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
    sleep(60)
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, clusterObj.getFirstAvaNode(caseName), timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
        
    for nodeObj in clusterObj.getNodes():
        nodeObj.setOsdPid(caseName)
        for osdObj in nodeObj.getOsds():
            osdObj.forceKill(caseName, nodeObj)
    
    for monObj in clusterObj.getMonitors():
        monObj.shutdown(caseName)
        monObj.start(caseName)
    for monObj in clusterObj.getMonitors():
        monObj.setMonPid(caseName)
        monObj.forceKill(caseName)
        
    #TBD:check IO
    for nodeObj in clusterObj.getNodes():
        for osdObj in nodeObj.getOsds():
            osdObj.start(caseName, nodeObj)
    
    for monObj in clusterObj.getMonitors():
        monObj.start(caseName)
    
    logging.getLogger(caseName).info("sleep 10 mins to wait cluster recover")    
    sleep(600)
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)  
    ''' 
    for client in clusterObj.getClients():
        base.stopIO(caseName, client) 
    '''
    for client in clusterObj.getClients():
        client.checkIOError(caseName) 
    logging.getLogger(caseName).info("case runs complete")
        
        
        