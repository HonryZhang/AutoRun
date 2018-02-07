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
from testcases.UI import osdstatus
import time
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
    sleep(2)
    loginlogout.changeEnglish(driver)  
    sleep(2)
    logging.getLogger(caseName).info("filter audit log with pre to now")
    #clusterManagement.filterEventLog(driver,  preTimeNum="6", preTimeUnit="Hours", source='denali2', service="cassandra", level="High", eventType="cpu-average")
    clusterManagement.filterAuditLog(caseName, driver, preTimeNum="6", preTimeUnit="Hours",  firstName='admin', lastName='admin')
    sleep(10)
    logging.getLogger(caseName).info("filter audit log with from to time")
    curTime = time.time()  
    fromTime=time.strftime('%m/%d/%Y',time.localtime(curTime))
    toTime=time.strftime('%m/%d/%Y',time.localtime(curTime+curTime%86400))
    clusterManagement.filterAuditLog(caseName, driver,  fromTime=fromTime, toTime=toTime)
    sleep(2)
    #osdstatus.checkOsdStatus (driver) 
    loginlogout.logout(caseName, driver)
    logging.getLogger(caseName).info("logout")
    driver.close()
 