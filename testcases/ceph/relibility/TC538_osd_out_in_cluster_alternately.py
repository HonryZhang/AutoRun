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
2. login the first node 
3. out all osds in sequence
4. stop all osds in sequence
5. start all osds in sequence
6. add in all osds in sequence
7. check the cluster status
8. repeat step 2-7 on the other node
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
            
    sleep(60)
    logging.getLogger(caseName).info("\nStep 2: Out the osd and check IO")
    for nodeObj in nodeList:
        for osdObj in nodeObj.getOsds():
            #out the osd
            for i in range(5):
                logging.getLogger(caseName).info("\nNow operate "+nodeObj.gethostName())
                logging.getLogger(caseName).info(len(nodeObj.getOsds()))
                logging.getLogger(caseName).info("\nNow operate "+osdObj.getid())
                logging.getLogger(caseName).info("out "+osdObj.getid())
                osdObj.outCluster(caseName, nodeObj)
                logging.getLogger(caseName).info("check if IO error")
                sleep(15)
                #add osd in cluster
                #logging.getLogger(caseName).info("add in "+osdObj.getid()+" to cluster")
                osdObj.inCluster(caseName, nodeObj)
                #check ceph health
                sleep(15)
            logging.getLogger(caseName).info("Now check if there is any IO error")   
            for client in clusterObj.getClients():
                client.checkIOError(caseName)
            for client in clusterObj.getClients():         
                if(client.checkIOProcess(caseName ) == "error"):
                    base.startRBDIO(caseName, client, imageNum, poolName)


    for client in clusterObj.getClients():
        client.checkIOError(caseName) 
    logging.getLogger(caseName).info("%s runs complete"%caseName)      
    
    
                