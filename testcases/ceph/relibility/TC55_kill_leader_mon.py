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
2. login the leader monitor, and kill the mon process
3. check cluster status, Io status and cluster quorum status
4. start another RBD, check contious IO
5. start the killed monitor
6. check cluster status, does the leader monitor will be back????
'''
newImageName = 'newRBD'


def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    
    #client = clusterObj.getClients()[0]
    nodeObj = clusterObj.getFirstAvaNode(caseName)
    
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
    for mon in clusterObj.getMonitors():
        mon.shutdown(caseName)
        mon.start(caseName)
    logging.getLogger(caseName).info("\nStep2: kill leader mon 10 times")
    for i in range(10):
        leaderMon = clusterObj.getLeaderMon()
        leaderMon.setMonPid(caseName)
        leaderMon.forceKill(caseName)
        #TBD: add try
        sleep(30)
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName)  
        #check monitor quorum status 
        leaderId = leaderMon.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        #create another rbd and start IO
        #clusterObj.createImg(caseName,size = '10G', pool = poolName, imageName = newImageName)
        #pid = client.writeRbdFio(caseName, newImageName, poolName)
    
        #start leader mon again
        leaderMon.start(caseName)
        leaderMon.checkIfMonStart(caseName)
        #TBD: add try
        sleep(60)
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("stop mon service on %s in cluster successfully"%nodeObj.gethostName())
        else:
            logging.getLogger(caseName).error("status is %s"%status)
            logging.getLogger(caseName).error("%s  runs failed"%caseName)
            status = clusterObj.getStatus(caseName, nodeObj, timeOut)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("stop in cluster successfully")
                
            else:
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                exit(-1)
        #check IO status
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName)    
        #check monitor quorum status
        leaderId = leaderMon.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        if(leaderId == leaderMon.gethostName()):
            logging.getLogger(caseName).info("%s is back"%leaderId)
        else:
            logging.getLogger(caseName).error("leader monitor %s is not back"%leaderId)
            exit(-1)
        for client in clusterObj.getClients():         
            if(client.checkIOProcess(caseName ) == "error"):
                base.startRBDIO(caseName, client, imageNum, poolName)    

            
    logging.getLogger(caseName).info("case runs complete")