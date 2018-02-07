from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.UI import *
import logging
import os, inspect
import base
port="3579"

caseDescription='''
UI test for invalid login
'''
def main(args):
    caseName = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    logging.getLogger(caseName).info(caseDescription)
    clusterObj = base.getClusterObj(caseName, args)
    nodeList = clusterObj.getNodes()
    options=driverSet.driverSet()
    driver = webdriver.Chrome(chrome_options=options)
    ip1=nodeList[0].getIpAddress()
    url =  "http://"+ip1+":"+port
    userName= nodeList[0].getUserName()
    passwd=nodeList[0].getPassword()
    driver.get(url)
    driver.maximize_window()
    sleep(2)
    loginlogout.login(caseName, driver, ip1,port, userName, passwd)   
    
    poolManagement.createPool(caseName, driver, 'UITestpool', '10')
    sleep(2)
    poolManagement.createBlockDeviceImg(caseName, driver, 'UITestpool', 'UITestImg', '5')
    sleep(2)
    poolManagement.createBlockDeviceSnap(caseName, driver, 'UITestImg', 'UITestSnap')
    sleep(2)
    logging.getLogger(caseName).info("create clone UITestClone on snap UITestSnap")
    poolManagement.createClone(caseName, driver, 'UITestSnap', 'UITestClone')
    sleep(2)    
    poolManagement.createBlockDeviceCloneSnap(caseName, driver, 'UITestClone', 'UITestCloneSnap')
    sleep(2)
    logging.getLogger(caseName).info("create clone with name UITestClonewithClone")
    poolManagement.createClone(caseName, driver, 'UITestCloneSnap', 'UITestClonewithClone')
    #poolManagement.createBlockDeviceSnap(caseName, driver,'UITestClone','newUITestSnap')
    sleep(2)
    logging.getLogger(caseName).info("flatten clone  UITestClonewithClone")
    poolManagement.flattenBlockDeviceClone(caseName, driver, 'UITestClonewithClone')
    sleep(10)
    logging.getLogger(caseName).info("delete clone UITestClonewithClone")
    poolManagement.deleteBlockDeviceImg(caseName, driver, 'UITestClonewithClone')
    sleep(2)
    logging.getLogger(caseName).info("delete snap UITestCloneSnap")
    poolManagement.deleteSnap(caseName, driver, 'UITestCloneSnap')
    sleep(2)
    logging.getLogger(caseName).info("delete clone UITestClone")
    poolManagement.deleteBlockDeviceClone(caseName, driver, 'UITestClone')
    sleep(2)
    logging.getLogger(caseName).info("delete snap UITestSnap")
    poolManagement.deleteSnap(caseName, driver, 'UITestSnap')  
    sleep(2)
    poolManagement.deleteBlockDeviceImg(caseName, driver, 'UITestImg')
    sleep(2)
    
    poolManagement.deletePool(caseName, driver, 'UITestpool')
    loginlogout.logout(caseName, driver)
    logging.getLogger(caseName).info("logout")
    driver.close()
 