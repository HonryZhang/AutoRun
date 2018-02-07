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
    #client = clusterObj.getClients()[0]
    nodeObj = clusterObj.getFirstAvaNode(caseName)
        
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, nodeObj, timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
        
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
        
    logging.getLogger(caseName).info("\nStep1: start IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startIO(caseName, client, 'nbd') 
    sleep(60)
    
    logging.getLogger(caseName).info("\nStep2: pause all osds")
    clusterObj.pauseOsd(caseName)
    status = clusterObj.getStatus(caseName, nodeObj, timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("pause cluster successfully")
    else:
        logging.getLogger(caseName).error("status is %s"%status)                
        logging.getLogger(caseName).error("print log for another 10 minutes")
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("resume cluster successfully")
            
        else:
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            exit(-1)
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startIO(caseName, client, 'nbd') 
    logging.getLogger(caseName).info("\nStep3: resume all osds")
    clusterObj.resumeOsd(caseName)
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startIO(caseName, client, 'nbd') 
    logging.getLogger(caseName).info("\nCase runs successfully")