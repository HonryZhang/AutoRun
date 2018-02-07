import logging
import sys
import re
import os
import commands
import paramiko
#from lib.ceph import *
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
import client
import monitors
import node
import pool
import utils
import osd

import subprocess
import remoteExecute
import logging

import time

class cluster(object):
    nodelist = [] #should be object later
    osdlist = []
    monlist = []
    clientlist = []
    
    def __init__(self, caseName, testEnvXml):
        #TBD update
        #self.nodelist = nodelist
        #self.monlist = monlist
        #Init the node
        testEnvTree = ET.parse(testEnvXml)
        treeRoot = testEnvTree.getroot()
        self.env_type = treeRoot.attrib['env_type']
        self.vboxbuildpath = treeRoot.find('builds/vboxbuildpath').text
        self.vagrantfile = treeRoot.find('builds/vagrantfile').text
        self.sdopd = treeRoot.find('builds/sdopd').text     
        self.clientlist = []
        self.nodelist = []
        self.monlist = []
        self.osdlist = []
        #Init client object       
        for clientInfo in treeRoot.findall('hardwares/clients/client'):
            clientId = clientInfo.attrib['id']
            ip_address = clientInfo.find('communication').attrib['ip_address']
            hostname = clientInfo.find('communication').attrib['hostname']
            password = clientInfo.find('communication').attrib['password']
            username = clientInfo.find('communication').attrib['username']
            clientObj = client.client(clientId, ip_address,hostname, password, username)
            self.clientlist.append(clientObj)
        #Init node object 
        for nodeInfo in  treeRoot.findall('hardwares/nodes/node'): 
            nodeId = nodeInfo.attrib['id']
            ip_address = nodeInfo.find('communication').attrib['ip_address']
            hostname = nodeInfo.find('communication').attrib['hostname']
            password = nodeInfo.find('communication').attrib['password']
            username = nodeInfo.find('communication').attrib['username']
            nodeObj = node.node(nodeId, ip_address, hostname, password, username)
            self.nodelist.append(nodeObj)        
        #Init monitors object 
        for monitorInfo in  treeRoot.findall('hardwares/monitors/monitor'): 
            monitorId = monitorInfo.attrib['id']
            ip_address = monitorInfo.find('communication').attrib['ip_address']
            hostname = monitorInfo.find('communication').attrib['hostname']
            password = monitorInfo.find('communication').attrib['password']
            username = monitorInfo.find('communication').attrib['username']
            #monitorObj = monitors.monitors(monitorId, ip_address, hostname, password, username)
            monitorObj = monitors.monitors(monitorId, ip_address, hostname, password, username)
            self.monlist.append(monitorObj) 
        #ssh to copy files from ceph nod
        print self.getMonitors()
        
        t = paramiko.Transport(self.monlist[0].getIpAddress(), '22')
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get('/etc/ceph/ceph.conf','/mnt/ceph.conf')
        #sftp.get('/etc/ceph/ceph.conf','E:\\ceph.conf')
        t.close()
        #paramiko.util.log_to_file("filename.log")
        #use ceph.conf file to init the cluster
        f = open('/mnt/ceph.conf')
        #f = open('E:\\ceph.conf')
        reg = r'^\[osd\.(\d*)\]$'
        osdRe = re.compile(reg)
        lines = f.readlines()

        for i in range(0, len(lines)):
            osdlist = osdRe.findall(lines[i])
            if (osdlist):
                i=i+1                
                hostname = lines[i].strip()
                hostname = hostname[7:]
                osdId = osdlist[0]
                #logging.getLogger(caseName).info(osdId)
                #logging.getLogger(caseName).info(hostname)
                osdObj = osd.osd(osdId,hostname)
                self.osdlist.append(osdObj)
        for nodeObj in self.nodelist:
            newOsdList = []
            for osdObj in self.osdlist:            
                if(nodeObj.gethostName() == osdObj.gethostName()):
                    newOsdList.append(osdObj)
            nodeObj.createOsds(newOsdList)
        #get monitor information
        leaderId = self.monlist[0].getQuorumLeader(caseName)
        for mon in self.monlist:
            if(leaderId == mon.gethostName()):
                mon.setleader()
                
    def setLeaderMon(self, leaderId):
        for mon in self.monlist:
            if(leaderId == mon.gethostName()):
                mon.setleader()
                
    def getLeaderMon(self):
        for mon in self.monlist:
            if(mon.getleader() == 1) :
                return mon
    def getFirstNonLeaderMon(self):
        for mon in self.monlist:
            if(mon.getleader() == 0) :
                return mon
                       
    def updateCluster(self, nodeObj):
        t = paramiko.Transport(nodeObj.getIpAddress(), '22')
        t.connect(username=nodeObj.getUserName(), password=nodeObj.getPassword())
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get('/etc/ceph/ceph.conf','/mnt/ceph.conf')
        #sftp.get('/etc/ceph/ceph.conf','E:\\ceph.conf')
        t.close()
        #use ceph.conf file to init the cluster
        f = open('/mnt/ceph.conf')
        #f = open('E:\\ceph.conf')
        reg = r'^\[osd\.(\d*)\]$'
        osdRe = re.compile(reg)
        lines = f.readlines()
        self.osdlist = []
        for i in range(0, len(lines)):
            osdlist = osdRe.findall(lines[i])
            if (osdlist):
                i=i+1                
                hostname = lines[i].strip()
                hostname = hostname[7:]
                osdId = osdlist[0]
                osdObj = osd.osd(osdId,hostname)
                self.osdlist.append(osdObj)
        for nodeObj in self.nodelist:
            newOsdList = []
            for osdObj in self.osdlist:            
                if(nodeObj.gethostName() == osdObj.gethostName()):
                    newOsdList.append(osdObj)
            nodeObj.createOsds(newOsdList)  
        #send the config file to other node
        for nodeObj in self.getNodes() :
            t = paramiko.Transport(nodeObj.getIpAddress(), '22')
            t.connect(username=nodeObj.getUserName(), password=nodeObj.getPassword())
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get('/etc/ceph/ceph.conf','/mnt/ceph.conf')
            #sftp.put('E:\\ceph.conf', '/tmp/ceph.conf')
            execmd = 'sudo -i mv /tmp/ceph.conf /etc/ceph/'
            remoteExecute.sshclient_execmd(nodeObj.getIpAddress(), nodeObj.getPort(), nodeObj.getUserName(), nodeObj.getPassword(), execmd)
            t.close()   
            
    def getClients(self):
        return self.clientlist
    
    def getNodes(self):
        return self.nodelist
    
    def getMonitors(self):
        return self.monlist
    
    def createOSD(self):
        #random pick a node to create osd   
        nodeIp = self.nodelist[0].getIpAddress()
        self.createOSDByNode(nodeIp)    
        return osd
    
    #TBD
    def createOSDByNode(self,nodeIp):
        cmd = "ssh denali@{node} 'kill osdid {id}'"
        (status, output)= commands.getstatusoutput(cmd.format(node=nodeIp))
        return osd
    
    def getFirstAvaNode(self, caseName):
        for node in self.getNodes():
            #print node.getIpAddress()
            exeCmd = "ping -c 3 "+ node.getIpAddress()+" | grep '0 received' | wc -l"
            pipe = subprocess.Popen(exeCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #Run with non-blocking method 
            sts = pipe.wait()
            result = pipe.stdout.read()
            if(result == '1\n'):
                Status = 1
                #print "ping "+node.getIpAddress()+" failed"
                logging.getLogger(caseName).info("ping "+node.getIpAddress()+" failed")
            else :
                Status = 0
                return node
            if (Status == 1):
                #print "No node is pingable, please check your environment"
                logging.getLogger(caseName).error("No node is pingable, please check your environment")
                exit(0)
                
    def getOsds(self):   
        return self.osdlist     
            
    def getStatus(self, caseName, node, timeout):        
        while(timeout>0):
            startTime = int(time.time())
            execmd = 'sudo -i ceph -s'
            logging.getLogger(caseName).info("execute command is "+execmd)
            result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
            logging.getLogger(caseName).info(result)
            if(result and len(re.findall(r'HEALTH_ERR', result)) >=1): 
                logging.getLogger(caseName).info("Now status is HEALTH_ERR, sleep 60s and try again ")
                time.sleep(60)
                continue
            else:
                resultList = result.split('\n') 
                '''               
                logging.getLogger(caseName).info(resultList[6])
                pgmapInfoList = resultList[8].split(':')
                pgNumberInfo = pgmapInfoList[0].split(',')
                logging.getLogger(caseName).info(pgNumberInfo[0])
                pgNumber =  re.sub('[^\d]','',pgNumberInfo[0].replace(" ", ""))
                logging.getLogger(caseName).info("PG number is "+pgNumber)
                usefulPGNumber = re.sub('[^\d]','',resultList[8].replace(" ", ""))
                logging.getLogger(caseName).info("usefull PG number is "+usefulPGNumber)
                '''
                for line in resultList:
                    if(len(re.findall(r'pgmap', line)) >=1):
                        pgmapInfoList = line.split(':')
                        pgNumberInfo = pgmapInfoList[1].split(',')
                        pgNumber =  re.sub('[^\d]','',pgNumberInfo[0].replace(" ", ""))
                    if(len(re.findall(r'active\+clean', line)) >=1):
                        usefulPGNumber = re.sub('[^\d]','',line.replace(" ", ""))
                
                logging.getLogger(caseName).info("PG number is "+pgNumber)
                logging.getLogger(caseName).info("usefull PG number is "+usefulPGNumber)
                        
                if(pgNumber == usefulPGNumber): 
                    return "HEALTH_OK"
            time.sleep(60)    
            currentTime = int(time.time())
            spendTime = currentTime - startTime
            timeout = timeout - spendTime
            logging.getLogger(caseName).info("cost %d seconds, left %d seconds when check the ceph status"%(spendTime, timeout))
        return "HEALTH_ERROR"
    
    def getMonStatus(self,caseName):
        execmd = 'sudo -i ceph mon stat'
        logging.getLogger(caseName).info("execute command is "+execmd)
        result = remoteExecute.sshclient_execmd(node.getIpAddress(), node.getPort(), node.getUserName(), node.getPassword(), execmd)
        return result
    
    def createPool(self,caseName, poolName, pgNumber ):  
        node = self.getFirstAvaNode(caseName)
        poolObj = node.createPool(caseName, poolName, pgNumber)
        return poolObj
    
    def getPoolByname(self, caseName, poolName):
        node = self.getFirstAvaNode(caseName)
        poolObj = node.getPoolByname(caseName, poolName)
        return poolObj
    
    def removePool(self, caseName, poolName):
        node = self.getFirstAvaNode(caseName)
        node.removePool(caseName, poolName)
    
    #size = 10G, pool = becky_Test, imageName = testImg
    def createImg(self, caseName, **kw):
        #Parser the arguments
        size = ''
        poolname=''
        imageName = ''
        for k,w in kw.iteritems():
            if (k == 'size'):
                size = w
            elif(k == 'pool'):
                poolname = w
            elif(k == 'imageName'):
                imageName = w
        if (not size) :
            size = '10G'
        if (not poolname):
            poolname = 'rbd'
        if(not imageName):
            imageName = 'image' 
        #node = self.getFirstAvaNode(caseName)
        clients = self.getClients()
        clients[0].createImg(caseName, size, poolname, imageName) 
    
    def removeImg(self, caseName, poolName, imageName):
        node = self.getFirstAvaNode(caseName)
        node.removeImg(caseName, poolName, imageName)
        
    def initOsdProcess(self, caseName): 
        for nodeObj in self.getNodes():
            nodeObj.initOsdProcess(caseName)
            status = self.getStatus(caseName, nodeObj, 6000)
            if(status == 'HEALTH_OK'):
                logging.getLogger(caseName).info("osd on node %s were init successfully"%nodeObj.gethostName())
            else:
                logging.getLogger(caseName).error("status is %s"%status)
                logging.getLogger(caseName).error("%s  runs failed"%caseName)
                status = self.getStatus(caseName, nodeObj, 6000)
                if(status == 'HEALTH_OK'):
                    logging.getLogger(caseName).info("osd on node %s were init successfully"%nodeObj.gethostName())
                else:
                    logging.getLogger(caseName).error("%s  runs failed"%caseName)
                    exit(-1)    
            
    def pauseOsd(self, caseName): 
        node = self.getFirstAvaNode(caseName)
        node.pauseOsd(caseName)
                 
    def resumeOsd(self,caseName):   
        node = self.getFirstAvaNode(caseName)
        node.resumeOsd(caseName) 
