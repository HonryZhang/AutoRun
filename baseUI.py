import re
import os
import commands
import paramiko
#from lib.ceph import *
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from lib.ceph import *

def initEnvironment(testEnvXml):
    testEnvTree = ET.parse(testEnvXml)
    treeRoot = testEnvTree.getroot()
    env_type = treeRoot.attrib['env_type']
    vboxbuildpath = treeRoot.find('builds/vboxbuildpath').text
    vagrantfile = treeRoot.find('builds/vagrantfile').text
    sdopd = treeRoot.find('builds/sdopd').text   
    
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