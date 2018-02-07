import os
import sys
import logging
import remoteExecute
import re

class monitors(object):
    monPid = ''
    port=22
    leader=0
    def __init__(self, id, ip_address,hostname, password, username, **kw):
        self.id = id
        self.ip_address = ip_address
        self.hostname = hostname
        self.password = password
        self.username = username
        for k,w in kw.iteritems():
            setattr(self,k,w)
        self.monPid = ''
        self.port=22
        self.leader=0
        
    def getIpAddress(self):
        return self.ip_address
    
    def getUserName(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def gethostName(self):
        return self.hostname
    
    def getMonPid(self):
        return self.monPid
    
    def getPort(self):
        return self.port
    
    def setMonPid(self, caseName):
        execmd = 'ps -ef | grep ceph-mon'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        logging.getLogger(caseName).info(resultList)
        for cephMonProcessInfo in resultList:
            cephMonProcessInfoList = cephMonProcessInfo.split()
            if(len (cephMonProcessInfoList) >= 10 and len(re.compile(r'bash -c ', re.I).findall(cephMonProcessInfo)) == 0):
                processId = cephMonProcessInfoList[1]
                self.monPid = processId
        logging.getLogger(caseName).info("mon pid is "+self.monPid)    
    
    def shutdown(self, caseName):  
        execmd = 'sudo -i stop ceph-mon id=' + self.gethostName()+" & sleep 5"
        logging.getLogger(caseName).info("mon is  "+self.gethostName()) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        if(len(re.findall(r'eph-mon stop\/waiting',result))==1):
            logging.getLogger(caseName).info("mon %s is shutdown successfully"%(self.gethostName()))
        else:
            logging.getLogger(caseName).error("Error when shutdown mon "+self.gethostName())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
            #exit(0)  
    
    def start(self, caseName):
        execmd = 'sudo -i ceph-mon -i ' + self.gethostName()+' & sleep 30' 
        logging.getLogger(caseName).info("mon is  "+self.gethostName())
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        #logging.getLogger(caseName).info("result is "+result)
        if(len(re.findall(r'continuing with monmap configuration',result))==1):
            logging.getLogger(caseName).info("mon %s is start successfully"%(self.gethostName()))
        else:
            logging.getLogger(caseName).error("Error when start mon "+self.gethostName())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            #exit(0) 
                     
    def stopService(self,caseName):
        execmd = "sudo -i kill "+self.getMonPid()+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        if(result and len(re.findall(r'is not a tty', result)) !=1):            
            logging.getLogger(caseName).error("Error when kill %s"+self.getid())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            #exit(0) 
    
    def forceKill(self, caseName):
        execmd = "sudo -i kill -9 "+self.getMonPid()+" & sleep 3"
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        #logging.getLogger(caseName).error(result)
        if(result and len(re.findall(r'is not a tty', result)) !=1):            
            logging.getLogger(caseName).error("Error when kill %s"+self.getid())
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)  
            #exit(0) 
    
    def checkIfMonStart(self, caseName):  
        execmd = "ps -ef | grep 'ceph-mon' "
        logging.getLogger(caseName).info("node is  "+self.gethostName())
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info(result)        
        resultList = result.split('\n')
        #logging.getLogger(caseName).info(resultList)
        if(len(resultList) == 3):
            logging.getLogger(caseName).info(self.gethostName()+" is not started, start again")
            self.start(caseName)
            return 0
        else:
            logging.getLogger(caseName).info(self.gethostName()+" is alrady started")
            return 1
        
    def setleader(self ):
        self.leader = 1
        
    def getleader(self):
        return self.leader
    
    def getQuorumLeader(self, caseName):
        execmd = "sudo -i ceph quorum_status --format json-pretty | grep quorum_leader_name"
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info(result) 
        resultList = result.split('\n')
        for leader in resultList:
            logging.getLogger(caseName).info(leader)
            if(len(re.findall(r'quorum_leader_name\"\: ', leader)) ==1):
                leaderId = leader.split(':')[1]                
                return leaderId.replace("\"", "").replace(",","").replace(" ", "")