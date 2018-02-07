import logging
import sys
import re
import os
import commands
import remoteExecute
import paramiko
from time import sleep
from testcases.ceph.relibility.glovar import *
#ssh root@192.168.28.105 'cat /proc/cpuinfo'
class osd(object):
    processId = ''
    disk = ''
    def __init__(self, id, hostName):
        self.processId = ''
        self.disk = ''
        self.id = 'osd.'+str(id)
        self.hostName = hostName
    
    def getid(self):
        return self.id
    
    def gethostName(self):
        return self.hostName

    def stop(self, caseName, node ):
        execmd = 'sudo -i stop ceph-osd id=' + self.getid().split('.')[1]+" & sleep 3"
        logging.getLogger(caseName).info("node is  "+node.gethostName()) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        if(len(re.findall(r'eph-osd stop\/waiting',result))==1):
            logging.getLogger(caseName).info("osd %s is shutdown successfully"%(self.id))
        else:
            logging.getLogger(caseName).error("Error when shutdown osd"+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
        
    def forceKill(self, caseName, node):
        execmd = "sudo -i kill -9 "+self.getProcessId()+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        if(result and len(re.findall(r'is not a tty', result)) !=1):            
            logging.getLogger(caseName).error("Error when kill %s"+self.getid())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
    
    def getMemory(self, caseName,  node):
        avaiMemory = '0GB'
        return avaiMemory
    
    def shutdown(self, caseName, node):
        execmd = "sudo -i kill "+self.getProcessId()+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        if(result and len(re.findall(r'is not a tty', result)) !=1):            
            logging.getLogger(caseName).error("Error when kill %s"+self.getid())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            
    def outCluster(self, caseName, node):
        execmd = "sudo -i ceph osd out "+self.id+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        print execmd
        print result
        if(len(re.findall(r'arked out', result)) ==1):
            logging.getLogger(caseName).info("%s is already out cluster"%(self.id))
            return
        else:
            logging.getLogger(caseName).error("Error when mark %s out"%(self.id))
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)

    
    def inCluster(self, caseName, node):   
        execmd = "sudo -i ceph osd in "+self.id+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        if(len(re.findall(r'arked in', result)) ==1):
            logging.getLogger(caseName).info("%s is already in cluster"%(self.id))
            return
        else:
            logging.getLogger(caseName).error("Error when mark %s in"%(self.id))
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)  
    
    def userStart(self,caseName, node): 
        execmd = 'sudo -i start ceph-osd id=' + self.id.split('.')[1]+' & sleep 30' 
        logging.getLogger(caseName).info("node is  "+node.gethostName())
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        #logging.getLogger(caseName).info("result is "+result)
        if(len(re.findall(r'ceph-osd * start/running',result))==1):
            logging.getLogger(caseName).info("osd %s is start successfully"%(self.id))
        else:
            logging.getLogger(caseName).error("Error when start osd"+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)   
                
    def start(self, caseName, node):
        execmd = 'sudo -i ceph-osd -i ' + self.id.split('.')[1]+' & sleep 30' 
        logging.getLogger(caseName).info("node is  "+node.gethostName())
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        #logging.getLogger(caseName).info("result is "+result)
        if(len(re.findall(r'tarting osd\.\d* at',result))==1):
            logging.getLogger(caseName).info("osd %s is start successfully"%(self.id))
        else:
            logging.getLogger(caseName).error("Error when start osd"+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
    
    def checkIfOsdStart(self, caseName, node):  
        execmd = "ps -ef | grep 'ceph-osd -i "+self.id.split('.')[1]+"'"
        logging.getLogger(caseName).info("node is  "+node.gethostName())
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        logging.getLogger(caseName).info(result)
        
        resultList = result.split('\n')
        #logging.getLogger(caseName).info(resultList)
        if(len(resultList) == 3):
            logging.getLogger(caseName).info(self.getid()+"has not started, start again")
            self.start(caseName, node)
            return 0
        else:
            logging.getLogger(caseName).info(self.getid()+"has already started")
            return 1
    
    def removeFromCrush(self, caseName, node):   
        execmd = "sudo -i ceph osd crush rm "+self.getid()+" & sleep 10"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'emoved item', result))==0):
            logging.getLogger(caseName).error("Error when remove osd from crush "+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
    
    def removeFromAuth(self, caseName, node):   
        execmd = "sudo -i ceph auth del "+self.getid()+" & sleep 10"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'pdated', result))==0):
            logging.getLogger(caseName).error("Error when delete osd from auth "+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)    
    
                      
    def delete(self, caseName, node):
        if (exeDir == '/usr/local/bin/scripts/create_cluster_scripts/bluestore/'):
            execmd = "sudo -i "+exeDir+"delete_osds_local.sh -n -d /dev/"+ self.disk
        elif(exeDir == '/usr/share/denali-ceph/'):
            execmd = "sudo -i "+exeDir+"ceph_delete_osds_local.sh -n -d /dev/"+ self.disk
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)        
        #logging.getLogger(caseName).info("execute command is "+result)
        if(len(re.findall(r'Delete osd successfully', result))==0):
            logging.getLogger(caseName).error("Error when delete "+self.getid())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            exit(0)
        return
    
    def removePartlable(self, caseName, node):
        execmd = "sudo -i parted -s -a optimal /dev/"+ self.disk+' mklabel gpt & sleep 30'
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        logging.getLogger(caseName).info(result)
        
    def forceDelete(self, caseName, node):
        self.forceKill(caseName, node)
        self.removeFromCrush(caseName, node)
        self.removeFromAuth(caseName, node)        
        execmd = "sudo -i ceph osd rm "+self.getid()+" & sleep 10"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        if(len(re.findall(r'emoved osd.', result))==0):
            logging.getLogger(caseName).error("Error when delete osd from "+self.id)
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
        sleep(30)
        self.removePartlable(caseName, node)
        self.updateCephConfig(caseName, node)    
        
    def updateCephConfig(self, caseName, node):  
        execmd = "sudo -i "+ exeDir+"updateCephConfig.sh [" + self.getid()+"]"
        logging.getLogger(caseName).info(execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
       
    def getStatus(self, caseName, node): 
        execmd = "sudo -i ceph osd find "+self.getid()+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd) 
        if(len(re.findall(r'error|failed', result))!=0):
            logging.getLogger(caseName).error("Error when get "+self.getid()+" status")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
        return result
    
    def setProcessId(self, processId):
        self.processId = processId
        
    def getProcessId(self):
        return self.processId  
    
    def getDisk(self):
        return self.disk
    
    def setDisk(self, disk):
        self.disk = disk
    