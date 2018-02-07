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
2. login the first node, force kill delete osd one by one
3. check IO status
'''


def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    logging.getLogger(caseName).info("init case")
    #clusterObj.initOsdProcess(caseName)
    
    #client = clusterObj.getClients()[0]
    
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
    sleep(60)
    
    nodeObj = clusterObj.getFirstAvaNode(caseName)
    nodeObj.initOsdProcess(caseName)
    
    nodeObj.setOsdDisk(caseName)
    disks = []
    for osdObj in nodeObj.getOsds():
        disks.append(osdObj.getDisk())
    nodeObj.uploadScript(caseName)
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, nodeObj, timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
    # = base.startIO(caseName)
    #sleep(60)   
     
    logging.getLogger(caseName).info("set pid process")
    nodeObj.setOsdPid(caseName)
    '''
    osdObj = nodeObj.getOsds()[0]
    disks.append(osdObj.getDisk())
    osdObj.forceDelete(caseName, nodeObj)        
    status = clusterObj.getStatus(caseName, nodeObj, timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("%s delete succesfully"%osdObj.getid())
    '''
    for osdObj in nodeObj.getOsds():
        #disks.append(osdObj.getDisk())
        osdObj.forceDelete(caseName, nodeObj)        
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("%s delete succesfully"%osdObj.getid())
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            status = clusterObj.getStatus(caseName, nodeObj, timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("kill in cluster successfully")
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)
    
    nodeObj.delete(caseName)
    clusterObj.updateCluster(nodeObj)     
    sleep (60)
        
    logging.getLogger(caseName).info("start to create osd on node %s "%nodeObj.gethostName())
    for disk in disks:        
        nodeObj.createOsd(caseName,disk)
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("%s create succesfully"%osdObj.getid())
    
    clusterObj.updateCluster(nodeObj)
    #nodeObj.initOsdProcess(caseName)
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    '''    
    logging.getLogger(caseName).info("all osd need to create on node %s create succesfully"%nodeObj.gethostName())
    for client in clusterObj.getClients():
        base.stopIO(caseName, client) 
    '''
    for client in clusterObj.getClients():
        client.checkIOError(caseName) 
    logging.getLogger(caseName).info("case runs complete")
    
           
        
    

        
        
        