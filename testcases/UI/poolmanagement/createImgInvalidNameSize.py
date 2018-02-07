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
create/delete pool, image, snap, clone
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
    sleep(2)
    logging.getLogger(caseName).info("create the pool with name UITestpool")
    poolManagement.createPool(caseName, driver, 'UITestpool', '10')
    driver.refresh()
    
    sleep(5)
    logging.getLogger(caseName).info("create the pool with invalid name UITestpool-")
    poolManagement.createPool(caseName, driver, 'UITestpool-', '10')
    driver.refresh()
    sleep(5)
    
    logging.getLogger(caseName).info("create the pool with invalid pool size -10")
    poolManagement.createPool(caseName, driver, 'UITestpoolinvalid', '-10')
    driver.refresh()
    sleep(5)
    #driver.refresh()
    logging.getLogger(caseName).info("create the image with invalid name UITestImg-")
    poolManagement.createBlockDeviceImg(caseName, driver, 'UITestpool', 'UITestImg-', '10', imgUnit='TB')
    driver.refresh()
    sleep(5)
    #driver.refresh()
    logging.getLogger(caseName).info("create the image with invalid size 01TB ")
    poolManagement.createBlockDeviceImg(caseName, driver, 'UITestpool', 'UITestImg', '01', imgUnit='TB')
    driver.refresh()
    #poolManagement.deleteBlockDeviceImg(caseName, driver, 'UITestImg')
    sleep(5)
    poolManagement.deleteBlockDeviceImg(caseName, driver, 'UITestImg')
    sleep(4)
    poolManagement.deletePool(caseName, driver, 'UITestpool')
    
    loginlogout.logout(caseName, driver)
    logging.getLogger(caseName).info("logout")
    driver.close()
 