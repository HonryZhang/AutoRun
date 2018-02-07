import os
import sys
import remoteExecute
import logging
import re
from lib.ceph import pool
import time
from testcases.ceph.relibility.glovar import *

class client(object):
    port=22
    def __init__(self, id, ip_address,hostname, password, username,**kw):
        self.id = id
        self.ip_address = ip_address
        self.hostname = hostname
        self.password = password
        self.username = username
        for k,w in kw.iteritems():
            setattr(self,k,w)
        
    def getIpAddress(self):
        return self.ip_address
    
    def getUserName(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def gethostName(self):
        return self.hostname  
        
    def getPort(self):
        return self.port
    
    def listMap(self, caseName):
        imageDiskDict = {}
        execmd = "sudo -i 'rbd-nbd' 'list-mapped'"
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info(result)
        resultList = result.split('\n')
        for imageList in resultList:
            if(len(re.compile(r'^\d', re.I).findall(imageList))!=0): 
                imageInfoList = re.split('\s*', imageList)
                imageDictKey = imageInfoList[1] + '_' + imageInfoList[2] 
                logging.getLogger(caseName).info('image is '+imageDictKey)
                imageDiskDict[imageDictKey] = imageInfoList[4]
                logging.getLogger(caseName).info('image mapped disk is  '+imageInfoList[4])
        return imageDiskDict
    
    def mapNbd(self, caseName, poolName, imageName):
        #list mapped, if mapped, return;else map
        imageDiskDict = {}
        imageDiskDict = self.listMap(caseName)
        imageKey = poolName+'_'+imageName
        if(imageDiskDict.has_key(imageKey)):
            logging.getLogger(caseName).info("image %s is already mapped to %s"%(imageKey, imageDiskDict[imageKey]))
            return imageDiskDict[imageKey]
        else:
            execmd = "sudo -i 'rbd-nbd' map "+ poolName + "/"+imageName
            result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
            if(len(re.compile(r'^dev\/*\d*', re.I).findall(result))!=0): 
                logging.getLogger(caseName).info("map disk successfully, new disk is %s"%result)
                result = '/'+re.findall(r"^dev\/nbd\d*", result)[0]
                logging.getLogger(caseName).info("disk is "+result)
                return result
            else:
                logging.getLogger(caseName).error("map error for %s"%imageName)
                logging.getLogger(caseName).error("execute command %s"%execmd)
                logging.getLogger(caseName).error("result is %s"%result) 
    
    def makeImageHash(self, caseName):
        return
    
    def unmapNbd(self, caseName, nbdName, disk):
        logging.getLogger(caseName).info("now unmap nbd "+nbdName) 
        execmd = "sudo -i rbd-nbd unmap "+ disk
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info("result %s"%result) 
        result = result.replace("\n", "").replace(" ","")
        if(result != "tdin:isnotatty"): 
            logging.getLogger(caseName).error("unmap error for %s"%nbdName)
            exit(-1)
        else:
            logging.getLogger(caseName).info("disk %s is umap successfully"%disk) 
        return
    
    def mkfs(self, caseName, disk, type):
        execmd = 'sudo -i  mkfs -t '+type+' '+disk
        logging.getLogger(caseName).info("exe command is: "+execmd) 
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')
        if(resultList[-2].replace(' ','') == 'done'):
            logging.getLogger(caseName).info("mkfs successfully") 
        execmd = 'sudo -i  mkdir /mnt/' + disk.split('/')[2]
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        execmd = 'sudo -i  mount ' +disk+' /mnt/'+ disk.split('/')[2]
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        return
    
    def writeNbdBlockIO(self,caseName, rate, disk, size):
        diskname = disk.replace("\/", "")
        execmd = 'nohup sudo -i fio -direct=1 -name='+ diskname +' -iodepth_batch_complete=1 -ioengine=libaio -bs=8k -rw=randwrite -verify_fatal=1 -verify=md5 -verify_interval=512 -verify_dump=1 -do_verify=1 -overwrite=1 -filename='+ disk+' -rate='+str(rate)+' -size='+size
        logging.getLogger(caseName).info("fio command is: "+execmd) 
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd, sync=False)
        #get pid of the fio thread
        execmd = 'ps -ef | grep '+disk
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')
        for pidInfo in resultList:
            pidInfoList = pidInfo.split()
            if(len (pidInfoList) > 10 and len(re.compile(r'bash -c', re.I).findall(pidInfo))==0):
                pidNumber = pidInfoList[1]
                logging.getLogger(caseName).info('pid info is '+pidNumber)
        return pidNumber
    
    def writeNbdFileIO(self,caseName, disk, fsType, size):
        self.mkfs(caseName, disk, fsType)        
        #size = baseSize        
        execmd = 'nohup sudo -i fio -direct=1 -name=nbdfiletest -iodepth=4 -overwrite=1 -nrfiles=100 -ioengine=libaio -bs=8k -rw=randwrite -verify=md5 -verify_fatal=1 -verify_interval=512 -verify_dump=1 -do_verify=1 -directory=/mnt/'+disk.split('/')[2]+' -size='+size
        logging.getLogger(caseName).info("fio command is: "+execmd) 
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd, sync=False)        
        execmd = 'ps -ef | grep '+disk
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        
        #TBD: To be update
        '''
        resultList = result.split('\n')
        for pidInfo in resultList:
            pidInfoList = pidInfo.split()
            if(len (pidInfoList) > 10 and len(re.compile(r'bash -c', re.I).findall(pidInfo))==0):
                pidNumber = pidInfoList[1]
                logging.getLogger(caseName).info('pid info is '+pidNumber)
        return pidNumber
        '''
    def createImg(self, caseName, size, poolName, imageName):   
        execmd = 'sudo -i rbd create '+imageName+'  --size '+size +' -p ' + poolName
        logging.getLogger(caseName).info(execmd) 
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info(result) 
        if(len(re.compile(r'error|failed|already exists|not found', re.I).findall(result))!=0):
            logging.getLogger(caseName).error("image %s create failed"%imageName) 
            exit(-1)
        else:
            logging.getLogger(caseName).info("image %s create successfully"%imageName)
            return imageName
    
    def removeImg(self, caseName, poolName, imageName):   
        execmd = 'sudo -i rbd rm '+poolName+'/'+imageName
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        print result
        if(len(re.compile(r'Removing image: 100% complete...done.', re.I).findall(result))!=0):
            logging.getLogger(caseName).info("image %s remove successfully"%imageName) 
        else:
            logging.getLogger(caseName).error("image %s delete error"%imageName)
                
    def writeRbdFio(self, caseName, imageName, poolName, size):
        #upload the rbd fio template into client
        #TBD: add runtime or not
        execmd = 'nohup sudo -i fio -direct=1 -iodepth_batch_complete=1 -ioengine=rbd -clientname='+self.gethostName()+' -pool='+poolName+' -rbdname='+imageName+' -rw=randwrite -bs=8K -size='+size+' -norandommap=1 -randrepeat=0 -verify=md5 -verify_fatal=1 -verify_dump=1 -do_verify=1 -overwrite=1 -iodepth=256 -name='+imageName
        #execmd = 'nohup sudo -i fio -ioengine=rbd -invalidate=0 -rw=randwrite -name='+imageName +' -bs=4k -verify=md5 -verify_fatal=1 -verify_interval=512 -verify_dump=1 -do_verify=1 -overwrite=1 -pool='+ poolName+' -rbdname='+imageName
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd, sync=False)
        logging.getLogger(caseName).info(execmd)
        #get pid of the fio thread
        execmd = 'ps -ef | grep '+imageName
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')
        '''
        for pidInfo in resultList:
            pidInfoList = pidInfo.split()
            if(len (pidInfoList) > 10 and len(re.compile(r'bash -c', re.I).findall(pidInfo))==0):
                pidNumber = pidInfoList[1]
                logging.getLogger(caseName).info('pid info is '+pidNumber)
        return pidNumber
        '''
    
    def stopFio(self, caseName):
        logging.getLogger(caseName).info("Stop io again")
        execmd = 'sudo -i killall fio -s 9 '
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        logging.getLogger(caseName).info(execmd)
        logging.getLogger(caseName).info(result)
        if(result and len(re.compile(r'no process found', re.I).findall(result))>=1):            
            logging.getLogger(caseName).error("Error when kill fio process")       
            logging.getLogger(caseName).error(result)
            exit(-1)
        return 0
    
    #def checkIOProcess(self, caseName, pidList):
    def checkIOProcess(self, caseName):
        execmd = 'sudo -i ps -ef | grep fio '
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')
        logging.getLogger(caseName).info(resultList)
        if(len(resultList) > 4):
            logging.getLogger(caseName).info('IO is running')
            return "ok"
        else:
            logging.getLogger(caseName).info('IO stopped')
            logging.getLogger(caseName).info('start IO again')
            #self.writeRbdFio(caseName, imageName, poolName)
            return "error"
        '''
        currentPidList = []
        for pidInfo in resultList:
            pidInfoList = pidInfo.split()
            if(len (pidInfoList) > 10 and len(re.compile(r'bash -c', re.I).findall(pidInfo))==0):
                pidNumber = pidInfoList[1]
                currentPidList.append(pidNumber)
                #logging.getLogger(caseName).info('pid info is '+pidNumber)
        pidList.sort()
        currentPidList.sort()
        if(pidList == currentPidList):
            return "OK"
        else:
            return "Error"
        '''
        
    def checkIOError(self, caseName):
        #execmd = 'sudo -i cd /root'
        #result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        #logging.getLogger(caseName).info(result)
        execmd = "sudo -i ls -ll /root | grep hdr_fail"
        result = remoteExecute.sshclient_execmd(self.getIpAddress(), self.getPort(), self.getUserName(), self.getPassword(), execmd)
        resultList = result.split('\n')
        if (len(resultList) > 2):
            logging.getLogger(caseName).error("IO verify failed")
            logging.getLogger(caseName).error(execmd)
            logging.getLogger(caseName).error(result)
            logging.getLogger(caseName).error("IO error, stop IO now")
            self.stopFio(caseName)
            exit(-1)
        return 
        