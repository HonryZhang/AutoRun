import os
import sys
import remoteExecute
import logging
import re
from lib.ceph import pool
import time
import paramiko
from unittest.loader import getTestCaseNames
from testcases.ceph.relibility.glovar import *
import pool
import osd

class node(object):
    port=22
    osdList =[]
    def __init__(self, id, ip_address, hostname, password, username, **kw):
        self.id = id
        self.ip_address = ip_address
        self.hostname = hostname
        self.password = password
        self.username = username
        for k,w in kw.iteritems():
            setattr(self,k,w)
        self.osdList =[]
        #super(node, self).__init__(type)
    
    def getIpAddress(self):
        return self.ip_address
    
    def getUserName(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getPort(self):
        return self.port
    
    def gethostName(self):
        return self.hostname   

    def addOsd(self,osd):
        self.osdList.append(osd)   
    
    def createOsds(self, osdlist):
        self.osdList =  osdlist[:] 
          
    def getOsds(self):
        #TBD:get available osd
        return self.osdList
    
    def getUpdateOsds(self):
        osdList = []
        osdIds = []
        execmd = 'ls -ll /dev/disk/by-partlabel/'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        osdDiskDict = {}
        for cephOsdDiskInfo in resultList:
            cephOsdDiskInfoList = cephOsdDiskInfo.split()
              
            if(len(re.findall(r'head-reverse-part|otal',cephOsdDiskInfo))== 0 and len(cephOsdDiskInfoList)>10):
                osdId = re.sub('\D','',cephOsdDiskInfoList[8]) 
                if(osdId not in osdIds):
                    osdIds.append(osdId) 
        for osdId in osdIds:           
            osdObj = osd.osd(osdId,self.gethostName())
            osdList.append(osdObj)
        self.osdList = osdList
        return self.osdList
    
    def createPool(self, caseName, poolName, pgNumber):
        execmd = 'sudo -i ceph osd pool create '+poolName+' '+str(pgNumber)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).error(result)
        if(len(re.compile(r'error|failed|already exists', re.I).findall(result))>0):
            logging.getLogger(caseName).error("pool %s created failed"%poolName) 
            logging.getLogger(caseName).error("Error message is %s"%result) 
            exit(0)
        elif (len(re.compile(r'created', re.I).findall(result))==1):
            #init a pool
            poolObj = pool.pool(poolName, pgNumber)
            logging.getLogger(caseName).info("pool %s created successfully"%poolName) 
            return poolObj
    
    def removePool(self, caseName, poolName):   
        execmd = 'sudo -i ceph osd pool rm '+poolName+' '+poolName+' --yes-i-really-really-mean-it'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        if(len(re.compile(r'error|failed', re.I).findall(result))!=0):
            logging.getLogger(caseName).error("pool %s remove failed"%poolName) 
        elif(len(re.compile(r'removed', re.I).findall(result))!=1):
            logging.getLogger(caseName).info("pool %s remove successfully"%poolName) 
            
    def getPoolByname(self, caseName, poolName):
        execmd = 'sudo -i ceph osd lspools '
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        print result
        if(len(re.findall(poolName, result))==1):
            logging.getLogger(caseName).info("pool %s was founded"%poolName) 
            execmd = 'ceph osd pool get '+poolName + ' pg_num'
            result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
            print result
            pgNumber= result.split()[1] 
            logging.getLogger(caseName).info("pgnumber is %s in  %s "%(pgNumber,poolName))
            poolObj = pool.pool(poolName, pgNumber)
            return poolObj       
        else:
            logging.getLogger(caseName).error("%s was not found"%poolName) 
            exit(0)
    

    '''
    For osd process init, we need to stop the process and start the process first before init, else
    the ceph-osd process will start automatically.  
    '''        
    def initOsdProcess(self, caseName):    
        logging.getLogger(caseName).info("init osd on node %s"%self.gethostName())    
        execmd = 'ps -ef | grep ceph-osd'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        osdProcessDict = {}
        for cephOsdProcessInfo in resultList:
            cephOsdProcessInfoList = cephOsdProcessInfo.split()
            if(len (cephOsdProcessInfoList) > 10):
                processId = cephOsdProcessInfoList[1]
                osdId = 'osd.'+cephOsdProcessInfoList[10]
                osdProcessDict[osdId] = processId
        for osdObj in self.getUpdateOsds():
            if osdProcessDict.has_key(osdObj.getid()):
                osdObj.setProcessId(osdProcessDict[osdObj.getid()])       
        for osdObj in self.getOsds():
            logging.getLogger(caseName).info("%s  ---> processId %s"%(osdObj.getid(), osdObj.getProcessId()))
        
        for osdObj in self.getOsds():
            osdObj.stop(caseName, self)
            time.sleep(5)
            osdObj.start(caseName, self)
            
        execmd = 'ps -ef | grep ceph-osd'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        osdProcessDict = {}
        for cephOsdProcessInfo in resultList:
            cephOsdProcessInfoList = cephOsdProcessInfo.split()
            if(len (cephOsdProcessInfoList) >= 10):
                processId = cephOsdProcessInfoList[1]
                osdId = 'osd.'+cephOsdProcessInfoList[9]
                osdProcessDict[osdId] = processId
        for osdObj in self.getOsds():
            if osdProcessDict.has_key(osdObj.getid()):
                osdObj.setProcessId(osdProcessDict[osdObj.getid()])       
        for osdObj in self.getOsds():
            logging.getLogger(caseName).info("%s  ---> processId %s"%(osdObj.getid(), osdObj.getProcessId()))
        
    def setOsdPid(self, caseName):
        execmd = 'ps -ef | grep ceph-osd'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        osdProcessDict = {}
        #logging.getLogger(caseName).info(resultList)
        for cephOsdProcessInfo in resultList:
            logging.getLogger(caseName).info(cephOsdProcessInfo)
            cephOsdProcessInfoList = cephOsdProcessInfo.split()
            if(len (cephOsdProcessInfoList) >= 10 and len(re.findall(r'bash',cephOsdProcessInfo))== 0):
                processId = cephOsdProcessInfoList[1]
                logging.getLogger(caseName).info(cephOsdProcessInfoList[9]) 
                osdId = 'osd.'+cephOsdProcessInfoList[9]
                if (cephOsdProcessInfoList[9].isdigit()):
                    osdProcessDict[osdId] = processId
        print osdProcessDict       
        for osdObj in self.getUpdateOsds():
            logging.getLogger(caseName).info(osdObj.getid()) 
            if osdProcessDict.has_key(osdObj.getid()):
                logging.getLogger(caseName).info(osdProcessDict[osdId]) 
                osdObj.setProcessId(osdProcessDict[osdObj.getid()])   
                   
        for osdObj in self.getOsds():
            logging.getLogger(caseName).info("%s  ---> processId %s"%(osdObj.getid(), osdObj.getProcessId()))
    
    def uploadScript(self, caseName):     
        t = paramiko.Transport(self.getIpAddress(), '22')
        t.connect(username=self.getUserName(), password=self.getPassword())
        sftp = paramiko.SFTPClient.from_transport(t)
        #upload the script
        scriptBasePath = os.path.abspath(sys.path[0])+"/config"
        changeCommon = scriptBasePath + "/changeCommon.sh"
        logging.getLogger(caseName).info(changeCommon)
        updateConfig = scriptBasePath + "/updateCephConfig.sh"
        logging.getLogger(caseName).info(updateConfig)
        sftp.put(changeCommon, "/tmp/changeCommon.sh")
        sftp.put(updateConfig, "/tmp/updateCephConfig.sh")
        t.close() 
        #change the script folder
        execmd = 'sudo -i mv /tmp/changeCommon.sh '+exeDir
        remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        execmd = 'sudo -i chmod +x '+exeDir+'/changeCommon.sh'  
        remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        execmd = 'sudo -i mv /tmp/updateCephConfig.sh '+exeDir
        remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        execmd = 'sudo -i chmod +x '+exeDir+'updateCephConfig.sh'  
        remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)  
    
       
    def setOsdDisk(self, caseName):
        execmd = 'ls -ll /dev/disk/by-partlabel/'
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')        
        osdDiskDict = {}
        for cephOsdDiskInfo in resultList:
            cephOsdDiskInfoList = cephOsdDiskInfo.split()
            logging.getLogger(caseName).info(cephOsdDiskInfo)    
            if(len(re.findall(r'head-reverse-part|otal',cephOsdDiskInfo))== 0 and len(cephOsdDiskInfoList)>10):
                osdId = re.sub('\D','',cephOsdDiskInfoList[8])
                logging.getLogger(caseName).info(osdId)
                logging.getLogger(caseName).info(cephOsdDiskInfo)                
                if (re.findall(r'nvme',cephOsdDiskInfoList[10])):
                    string = cephOsdDiskInfoList[10]
                    string = re.sub('\..\/','',string)
                    disk = re.split('p', string)[0]
                else:
                    disk = re.sub('\..\/|\d$','',cephOsdDiskInfoList[10])

                logging.getLogger(caseName).info(disk)
                osdId = 'osd.'+osdId
                osdDiskDict[osdId] = disk
        print osdDiskDict
        for osdObj in self.getUpdateOsds():
            if osdDiskDict.has_key(osdObj.getid()):
                osdObj.setDisk(osdDiskDict[osdObj.getid()])      
        for osdObj in self.getOsds():
            logging.getLogger(caseName).info("%s  ---> disk %s"%(osdObj.getid(), osdObj.getDisk()))
        return 
    
    def createOsd(self, caseName, disk):
        execmd = "sudo -i "+exeDir+"changeCommon.sh "+ disk
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        if (exeDir == '/usr/local/bin/scripts/create_cluster_scripts/bluestore/'):
            execmd = "sudo -i "+exeDir+"create_osds_local.sh -f "
        elif(exeDir == '/usr/share/denali-ceph/'):
            execmd = "sudo -i "+exeDir+"ceph_create_osds_local.sh -f "
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'successfully', result))==0):
            logging.getLogger(caseName).error("Error when create osd")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
            exit(0)               
        return
    
    def pauseOsd(self, caseName):
        execmd = "sudo -i ceph osd set pause"
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'pauserd,pausewr is set', result))==0):
            logging.getLogger(caseName).error("Error when pause cluster")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result) 
            exit(0)         
        return
    
    def resumeOsd(self, caseName):
        execmd = "sudo -i ceph osd unset pause"
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'pauserd,pausewr is unset', result))==0):
            logging.getLogger(caseName).error("Error when pause cluster")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            exit(0)   
        return  
    
    def delete(self, caseName):
        execmd = "sudo -i ceph osd crush remove "+self.gethostName()
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd) 
        logging.getLogger(caseName).info("execute command is "+execmd)
        logging.getLogger(caseName).info(result)
        if(len(re.findall(r'removed item id ', result))==0):
            logging.getLogger(caseName).error("Error when pause cluster")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            exit(0)   
        return 
    
    def checkContinousIO(self, caseName):
        execmd = "iostat -d -k 10 20 > iostat_status1 "
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        time.sleep(60)
        execmd = "iostat -d -k 10 20 > iostat_status2 "
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info("start to diff two io status")  
        execmd = "diff iostat_status1 iostat_status2 "
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        if(result):
            logging.getLogger(caseName).error("No continous IO")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            exit(0)  
            