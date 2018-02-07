from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import element

def checkOsdStatus(caseName, driver):
    logging.getLogger(caseName).info( "Check osd status")
    osdInfoList=[]
    sleep(1)
    driver.find_element_by_id(element.GOTO_OSD).click() 
    sleep(2)
    driver.find_element_by_xpath("//a[@href='/tbd/osd/status']").click()
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_OSD_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    #TBD: check the host is right with backend or not
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info( driver.find_element_by_xpath("//*[@id='CEPH_OSD_LIST_TABLE']/tbody/tr[%s]/td[2]/a"%(i)).text)
        driver.find_element_by_xpath("//*[@id='CEPH_OSD_LIST_TABLE']/tbody/tr[%s]/td[2]/a"%(i)).click()
        sleep(1)
        osdCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr"))
        logging.getLogger(caseName).info( osdCount )
        for j in range(1, osdCount+1):
            try:
                osdNum = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[2]"%(j)).text
            except:
                osdNum = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[2]"%(j)).text
            try:
                osdStatus = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[3]/span[1]"%(j)).text
            except:
                osdStatus = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[3]/span[1]"%(j)).text
            try:
                weight = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[4]"%(j)).text
            except:
                 weight = driver.find_element_by_xpath("//*[@id='CEPH_OSD_DETAIL_LIST_TABLE']/tbody/tr[%s]/td[4]"%(j)).text
                 
            osdInfo = osdNum+'_'+osdStatus+'_'+weight
            osdInfoList.append(osdInfo)
            logging.getLogger(caseName).info( osdInfo)
        driver.find_element_by_id(element.GOTO_OSD).click() 
        sleep(2)
        driver.find_element_by_xpath("//a[@href='/tbd/osd/status']").click()
    return osdInfoList

'''   
if __name__=="__main__":
    from lib.UI import loginlogout
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    
    ip1="192.168.28.171"
    port="3579"
    url =  "http://"+ip1+":"+port
    driver.get(url)
    loginlogout.login(driver, ip1,port)
    checkOsdStatus (driver) 
'''