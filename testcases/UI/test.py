from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.UI import *
import base
import logs
import logging
import os, inspect

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

ip1="192.168.28.171"
port="3579"
url =  "http://"+ip1+":"+port
driver.get(url)
loginlogout.login(driver, ip1,port)
poolName='UITestPool'
poolCapcity='15'
imgName='bkImg'
imgSize='100'
imgNum='10'
snapName="snapUITest"
cloneName="cloneUITest"
snapNum='3'
interval='3'
snapScheduleName='snapSchedule'
caseDescription = '''
This test case will do the following steps:
1. start IO on 10 images with randwrite and verify
2. login the first node 
3. out all osds in sequence
4. stop all osds in sequence
5. start all osds in sequence
6. add in all osds in sequence
7. check the cluster status
8. repeat step 2-7 on the other node
'''
def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args) 
    osdInfoList = osdStatus.checkOsdStatus(driver)
#replicaNum='2'
#goToAccountSettings()
#changeProfilePhoto()
    poolManagement.createPool(driver,poolName, poolCapcity)
#driver.refresh()
#createBlockDeviceImg(poolName=poolName,imgName=imgName, imgSize=imgSize)
#driver.refresh()
#setSnap(imgName=imgName, snapName=snapName, snapNum=interval)
#driver.refresh()
#deleteScheduleSnap()
#createBlockDeviceSnap(imgName=imgName, snapName=snapName)
#poolManagement.createScheduleSnap(driver, imgName, snapScheduleName,interval)
#poolManagement.deleteScheduleSnap(driver, snapScheduleName)

#createClone(snapName=snapName, cloneName=cloneName)
#flattenBlockDeviceClone(cloneName=cloneName)
#deleteScheduleSnap()
#batchCreateBlockDeviceImg(imgName=imgName, imgSize=imgSize,imgNum=imgNum)
#deleteBlockDeviceSnap()
#deleteBlockDeviceImg(imgName=imgName)
#batchDeleteBlockDeviceImg(imgNum=imgNum)
#driver.refresh()
#logout()
#login(ip1="192.168.28.113",port="3579")
#deletePool()
    driver.refresh()
    loginlogout.logout(driver)