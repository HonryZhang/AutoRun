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
3. stop all osds in sequence
4. start all osds in sequence
5. check the cluster status
6. repeat step 2-5 on the other node
'''

def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    logging.getLogger(caseName).info("the timeout is %d"%timeOut)
    clusterObj = base.getClusterObj(caseName, args)
    clusterObj.initOsdProcess(caseName)
    nodeList = clusterObj.getNodes()
    #client = clusterObj.getClients()[0]
    
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, clusterObj.getFirstAvaNode(caseName), timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
       
    logging.getLogger(caseName).info("\nStep 1: start IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startIO(caseName, client, 'nbd') 
    sleep(60)
    
    logging.getLogger(caseName).info("\nStep 2: stop osd and check IO")
    #logging.getLogger(caseName).info("\n%d"%len(nodeList))
    for nodeObj in nodeList:
        logging.getLogger(caseName).info("\nNow operate osd on %s"%(nodeObj.gethostName()))        
        for osdObj in nodeObj.getOsds():
            #out the osd
            logging.getLogger(caseName).info("\nNow operate "+osdObj.getid())
            #stop osd service
            
            logging.getLogger(caseName).info("Set the "+osdObj.getid()+" pid for kill")
            nodeObj.setOsdPid(caseName)
            logging.getLogger(caseName).info("shutdown "+osdObj.getid()+" by kill")
            osdObj.shutdown(caseName, nodeObj)
            for client in clusterObj.getClients():
                client.checkIOError(caseName)
            #start osd service
            logging.getLogger(caseName).info("start "+osdObj.getid())
            osdObj.start(caseName, nodeObj)
            returnCode = osdObj.checkIfOsdStart(caseName, nodeObj)
            tryCount = 0
            while(returnCode == 0 and tryCount < 10):
                returnCode = osdObj.checkIfOsdStart(caseName, nodeObj)
                tryCount = tryCount+1
            if (tryCount == 10):
                logging.getLogger(caseName).error("%s cannot start"%osdObj.getid())

            #check ceph health
            sleep(30)
            for client in clusterObj.getClients():
                client.checkIOError(caseName)
            status = clusterObj.getStatus(caseName, nodeObj, timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("stop %s in cluster successfully"%osdObj.getid())
            else:
                logging.getLogger(caseName).error("status is %s"%status)                
                logging.getLogger(caseName).error("print log for another 10 minutes")
                status = clusterObj.getStatus(caseName, nodeObj, timeOut)
                if(status == 'HEALTH_OK'):
                    logging.getLogger(caseName).info("stop %s in cluster successfully"%osdObj.getid())
                    break
                else:
                    logging.getLogger(caseName).error("%s  runs failed"%caseName)
                    exit(-1)
            
            for client in clusterObj.getClients():
                client.checkIOError(caseName)
            for client in clusterObj.getClients():         
                if(client.checkIOProcess(caseName ) == "error"):
                    base.startIO(caseName, client, 'nbd') 
  
    logging.getLogger(caseName).info("%s runs complete"%caseName)      
    