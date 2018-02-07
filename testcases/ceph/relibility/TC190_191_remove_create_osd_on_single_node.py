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
3. remove the osd one by one on the first node
4. check the status
5. create osd on the node
'''
def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    avaiNode = clusterObj.getFirstAvaNode(caseName)
    #client = clusterObj.getClients()[0]
    
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, clusterObj.getFirstAvaNode(caseName), timeOut)
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
    
    avaiNode.uploadScript(caseName)
    osdlist = avaiNode.getOsds()
    for osdObj in osdlist:
        osdObj.forceKill(caseName, avaiNode)
        osdObj.userStart(caseName, avaiNode)
        
    sleep(60)
    logging.getLogger(caseName).info("\nStep2: remove osd and create them 10 times")
    for i in range(10):
        avaiNode.setOsdDisk(caseName)        
        disks = []
        logging.getLogger(caseName).info("start to delete osd on node %s "%avaiNode.gethostName())
        for osdObj in avaiNode.getOsds():
            disks.append(osdObj.getDisk())
            osdObj.delete(caseName, avaiNode)
            status = clusterObj.getStatus(caseName, avaiNode, timeOut)
            logging.getLogger(caseName).info("sleep 600s to wait the pg transfer successfully")
            sleep(600)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("%s delete succesfully"%osdObj.getid())
            else:
                logging.getLogger(caseName).error("status is %s"%status)
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                status = clusterObj.getStatus(caseName, avaiNode, timeOut)
                if(status == 'HEALTH_OK'):
                    logging.getLogger(caseName).info("stop in cluster successfully")
                else:
                    logging.getLogger(caseName).error("%s  runs failed"%caseName)
                    exit(-1)    
        for client in clusterObj.getClients():
            client.checkIOError(caseName)        
        clusterObj.updateCluster(avaiNode)
        logging.getLogger(caseName).info("all osds on node %s delete succesfully"%avaiNode.gethostName())
        
        logging.getLogger(caseName).info("start to create osd on node %s "%avaiNode.gethostName())
        for disk in disks:        
            avaiNode.createOsd(caseName,disk)
            status = clusterObj.getStatus(caseName, avaiNode, timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("%s create succesfully"%osdObj.getid())
            else:
                logging.getLogger(caseName).error("status is %s"%status)
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                status = clusterObj.getStatus(caseName, avaiNode, timeOut)
                if(status == 'HEALTH_OK'):
                    logging.getLogger(caseName).info("stop in cluster successfully")
                else:
                    logging.getLogger(caseName).error("%s  runs failed"%caseName)
                    exit(-1) 
                    
            for client in clusterObj.getClients():
                client.checkIOError(caseName)
            for client in clusterObj.getClients():         
                if(client.checkIOProcess(caseName ) == "error"):
                    base.startIO(caseName, client, 'nbd') 
            
        clusterObj.updateCluster(avaiNode)
        logging.getLogger(caseName).info("all osd need to create on node %s create succesfully"%avaiNode.gethostName())
     
    logging.getLogger(caseName).info("case runs complete")
    return 1
 