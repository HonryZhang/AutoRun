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
UI test for user account change email
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

    
    Setting.emailSetting(caseName, driver, enable="1", smtpAddress="smtp.office365.com", smtpRelayPort="587", enableSmtpAuth="1", userName="lin", passwd="li",enableSenderAddress="from_address@istuary.com", subject="event notification", notification="Batch All", operation="save")
    
    sleep(1)
    loginlogout.logout(caseName, driver)
    logging.getLogger(caseName).info("logout")
    driver.close()