import urllib
import re
import sys
import getopt
import os
import commands
import pexpect
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

#myurl="http://192.168.28.48:3579/initialize"
ipsecond=""
ipthird=""
import time
imageName = ''
stream = ''
build = 'virtualbox'
#url = ''
help  = False
IPList = []
initFile = 'init.txt'
'''
usage: python cluster_init.py -n /home/becky/ubuntu/XXX.box -b virtualbox -s denali-ubuntu-CN
-n image save path, should be absolute path
-b virtual box or iso
-s stream, should be searched from http://192.168.28.96/istuary 
'''
def getOpts():
    global imageName
    global stream
    global build
    global help
    options, remainder = getopt.getopt(sys.argv[1:], 'n:s:b:h', ['imagename=', 
                                                     'stream=',
                                                     'build='
                                                     'help'
                                                     ])
    for opt, arg in options:
        if opt in ('-n', '--imagename'):
            imageName = arg
        elif opt in ('-s','--stream'):
            stream = arg
        elif opt in ('-b','--build'):
            build = arg
        elif opt in ('-h','--help'):
            help = True
    print help
    if(len(imageName) == 0 or len(stream) == 0) and (not help):
        print "The parameter you entered is invalid, please use -h or --help for help"
        exit()
    if(help):
        print "Welcome to use this tool to install and initialize the cluster environment"
        print "-n: imagename, image name you saved"
        print "-b: build,  virtualbox or iso"
        print "-s: stream, stream name"
        exit()

def clearEnvironment():
    print "clear environment"
    os.system('vagrant destroy -f')   
    os.system('vagrant box remove default')
        
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getDownloadImage(html):
    if (build == 'virtualbox'):
        reg = r'href="(.+?\.box)">virtualbox'
        downloader = re.compile(reg)
        downloadList = re.findall(downloader, html)
        #print "there are %d virtuallist in total"%len(downloadList)
        print "The latest download url is "+downloadList[0]
        urllib.urlretrieve(downloadList[0],imageName)
        return downloadList
    elif(build == 'iso'):
        return 0
        
def initUrl():
    if (build == 'virtualbox'):
        url = 'http://192.168.28.96/istuary/'+stream
        return url
    elif(build == 'iso'):
        #TBD
        url = 'http://192.168.28.96/istuary/'+stream    
        
def vboxAdd():
    print "Now start to add virtualbox"
    os.chdir(os.path.dirname(imageName))
    cmd = 'vagrant box add default ' + os.path.basename(imageName)
    print cmd
    os.system(cmd)   

def vboxUp():
    print "Now start to vagrant up the vm"
    os.system('vagrant up') 

def getVmName():
    print "Now start to get the vm name"
    cmd = 'vagrant status'
    (status, output)= commands.getstatusoutput(cmd)
    vmNames = re.findall(r'Denali\d+', output)
    print output
    print "name is "+ vmNames[0]+vmNames[1]
    return vmNames
    #parser the result
def getVmIP(hostName): 
    print "Now start to get vm IP address"
    cmd = "vagrant ssh "+ hostName +" -c 'ip a'"
    print cmd    
    (status, output)= commands.getstatusoutput(cmd)
    print output
    #parser the ip address
    obtain_ip = re.findall(r'192\.168\.\d+.\d+', output)
    return obtain_ip[0]

def addGw(hostName, ip):
    print "Now add the gateway"
    cmd = "vagrant ssh {hostName} -c 'sudo route add default gw {ip}'"
    (status, output)= commands.getstatusoutput(cmd.format(hostName=hostName, ip=ip))  


def initilization(IPList):
    global initFile
    print "Now start to initialize the cluster"
    pCommand = "pybot -v IP_Address1:"+IPList[0]+" -v IP_Address2:"+IPList[1]+" -v IP_Address3:"+IPList[2]
    #pCommand = "pybot -v IP_Address1:192.168.28.76 -v IP_Address2:192.168.28.77 -v IP_Address3:192.168.28.78"
    pCommand = pCommand +' '+ os.path.dirname(imageName)+'/'+initFile
    host = 'localhost'
    user = 'root'
    password = 'Denali@123'
    print pCommand 
    os.system(pCommand) 

def runUIcases(IPList): 
    
    return
def ssh_command (user, host, password, command):
    """
    This runs a command on the remote host. This could also be done with the
    pxssh class, but this demonstrates what that class does at a simpler level.
    This returns a pexpect.spawn object. This handles the case when you try to
    connect to a new host and ssh asks you if you want to accept the public key
    fingerprint and continue connecting.
    """
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s'%(user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        return None
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0: # Timeout
            print 'ERROR!'
            print 'SSH could not login. Here is what SSH said:'
            print child.before, child.after
            return None
    child.sendline(password)
    return child
#getVmName()
getOpts()

clearEnvironment()
url = initUrl()    
print "url is "+url
html = getHtml(url)

getDownloadImage(html)

vboxAdd()
vboxUp()

vmNames = getVmName()

for vmName in vmNames:
    ip = getVmIP(vmName)
    addGw(vmName, ip)
    IPList.append(ip)
print IPList

#IPList = ['192.168.28.78','192.168.1.1','192.168.28.76']
#myurl="http://"+IPList[0]+":3579/initialize"
#uiinit(newurl=myurl,ip2=IPList[1],ip3=IPList[2])
initilization(IPList)

runUIcases(IPList)

