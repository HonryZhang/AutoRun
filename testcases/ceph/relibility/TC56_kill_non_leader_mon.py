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
2. login the non-leader monitor, and kill the mon process
3. check cluster status, Io status and cluster quorum status
4. start the killed monitor
5. check cluster status, does the leader monitor will be back????
'''
newImageName = 'newRBD'


def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    
    #client = clusterObj.getClients()[0]
    nodeObj = clusterObj.getFirstAvaNode(caseName)
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
    sleep(60)
    
    nonLeaderMon = clusterObj.getFirstNonLeaderMon()
    nonLeaderMon.shutdown(caseName)
    nonLeaderMon.start(caseName)
    logging.getLogger(caseName).info("\nStep2: kill non-leader mon 10 times")
    for i in range(10):
        nonLeaderMon.setMonPid(caseName)
        nonLeaderMon.forceKill(caseName)
        sleep(30)
        for client in clusterObj.getClients(): 
            client.checkIOError(caseName) 
        #check monitor quorum status 
        leaderIdBefore = nonLeaderMon.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now deal the non-leader mon  %s"%leaderIdBefore)
        #create another rbd and start IO
        #clusterObj.createImg(caseName,size = '10G', pool = poolName, imageName = newImageName)
        #pid = client.writeRbdFio(caseName, newImageName, poolName)
        '''
        pidList = []
        pidList.append(pid)
        if (client.checkIOProcess(caseName, pidList) == 'Error'):
            logging.getLogger(caseName).error("IO cannot start")
            exit
        '''
        #start leader mon again
        nonLeaderMon.start(caseName)
        nonLeaderMon.checkIfMonStart(caseName)
        sleep(30)
        status = clusterObj.getStatus(caseName, nodeObj, timeOut)
        if(status == 'HEALTH_OK'):
            logging.getLogger(caseName).info("stop mon service on %s in cluster successfully"%nonLeaderMon.gethostName())
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
        leaderIdAfter = nonLeaderMon.getQuorumLeader(caseName)
        logging.getLogger(caseName).info("now the leader mon is %s"%leaderIdAfter)
        if(leaderIdBefore == leaderIdAfter):
            logging.getLogger(caseName).info("the leader mon is not impacted")
        else:
            logging.getLogger(caseName).error("the leader mon is not the initial one")
            exit(-1)
        for client in clusterObj.getClients():         
            if(client.checkIOProcess(caseName ) == "error"):
                base.startRBDIO(caseName, client, imageNum, poolName)   
                 
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    logging.getLogger(caseName).info("case runs complete")