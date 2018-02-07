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
4. login the new leader monitor, and kill the mon process
5. check cluster status, Io status and cluster quorum status
6. start the first killed monitor
7. check cluster status, does the leader monitor will be back????
8. start the first killed monitor
9. check cluster status, does the leader monitor will be back????
'''
#newImageName = 'newRBD'


def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    
    logging.getLogger(caseName).info("start to check cluster status before case running")
    status = clusterObj.getStatus(caseName, clusterObj.getFirstAvaNode(caseName), timeOut)
    if(status == 'HEALTH_OK'):
        logging.getLogger(caseName).info("health status is OK")
        
    else:
        logging.getLogger(caseName).error("health status is error")
        exit(-1)
        
    #client = clusterObj.getClients()[0]
    nodeObj = clusterObj.getFirstAvaNode(caseName)
    logging.getLogger(caseName).info("\nStep1: start IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startIO(caseName, client, 'nbd') 
    sleep(60)
    
    logging.getLogger(caseName).info("\nStep2: kill leader mon 10 times")    
    leaderMonFir = clusterObj.getLeaderMon()
    leaderMonSec = clusterObj.getLeaderMon()
    leaderMonFir.shutdown(caseName)
    leaderMonFir.start(caseName)
    leaderMonSec.shutdown(caseName)
    leaderMonSec.start(caseName)
    for i in range(10):        
        leaderMonFir.setMonPid(caseName)
        leaderMonFir.forceKill(caseName)
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName)
        #TBD: add try
        sleep(30)
        #check monitor quorum status 
        leaderId = leaderMonFir.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        clusterObj.setLeaderMon(leaderId)
        
        leaderMonSec.setMonPid(caseName)
        leaderMonSec.forceKill(caseName)
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName)
        #TBD: add try
        sleep(30)
        #check monitor quorum status 
        leaderId = leaderMonSec.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        clusterObj.setLeaderMon(leaderId)
        
            #start leader second mon again
        leaderMonSec.start(caseName)
        leaderMonSec.checkIfMonStart(caseName)
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
        leaderId = leaderMonSec.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        if(leaderId == leaderMonSec.gethostName()):
            logging.getLogger(caseName).info("%s is back"%leaderId)
        else:
            logging.getLogger(caseName).error("leader monitor %s is not back"%leaderId)
            exit(-1)
        clusterObj.setLeaderMon(leaderId)
        
        #start leader first mon again
        leaderMonFir.start(caseName)
        leaderMonFir.checkIfMonStart(caseName)
        #TBD: add try
        sleep(60)
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName)
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
        for client in clusterObj.getClients():         
            if(client.checkIOProcess(caseName ) == "error"):
                base.startIO(caseName, client, 'nbd')     
        #check monitor quorum status
        leaderId = leaderMonFir.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderId)
        if(leaderId == leaderMonFir.gethostName()):
            logging.getLogger(caseName).info("%s is back"%leaderId)
        else:
            logging.getLogger(caseName).error("leader monitor %s is not back"%leaderId)
            exit(-1)
        clusterObj.setLeaderMon(leaderId)    

        
    logging.getLogger(caseName).info("case runs complete")
    
    