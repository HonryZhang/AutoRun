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
2. login the mon node 
3. stop mon service
4. start mon service
'''

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
    logging.getLogger(caseName).info("\nStep1: Check IO from clients")
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    for client in clusterObj.getClients():         
        if(client.checkIOProcess(caseName ) == "error"):
            base.startRBDIO(caseName, client, imageNum, poolName)
            
    sleep(60)

    monitors = clusterObj.getMonitors()
    monitors[0].setMonPid(caseName)
    monitors[0].shutdown(caseName)
    sleep(30)
    #TBD:check if io process is still exist
    '''
    if(client.checkIOProcess(caseName, pidList) == 'Error') :
        logging.getLogger(caseName).error("some process is wrong")
    '''
    monitors[0].start(caseName)
    monitors[0].checkIfMonStart(caseName)
    sleep(30)
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
        
    #logging.getLogger(caseName).info("\nstop IO from clients") 
    #sleep(60)  
    for client in clusterObj.getClients():
        client.checkIOError(caseName)
    '''
    for client in clusterObj.getClients():          
        base.stopIO(caseName, client) 
    '''
    logging.getLogger(caseName).info("\ncase runs complete")
    
    
    
    
