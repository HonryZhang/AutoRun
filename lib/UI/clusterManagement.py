from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.UI import loginlogout
import logging
import element

# element.GOTO_CLUSTERMGMT
def addNode(caseName, driver,ip):
    logging.getLogger(caseName).info( "add nodes")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_CLUSTERSETTING).click() 
    sleep(5)
    driver.find_element_by_id(element.CLUSTER_ADD_SERVER_BUTTON).click()
    sleep(5)
    driver.find_element_by_id("INITIALIZE_IP_ADDRESS_INPUT0").click()
    driver.find_element_by_id("INITIALIZE_IP_ADDRESS_INPUT0").send_keys(ip)
    sleep(5)
    try:
        errElements = driver.find_elements_by_xpath("//div[contains(@class, 'ipaddress-error-inline-div')]")
        logging.getLogger(caseName).info( len(errElements))
        if(len(errElements) > 0):
            logging.getLogger(caseName).info("IP address is illegal")
            return
    except:
        logging.getLogger(caseName).info( "IP address is right")
    sleep(5)
    driver.find_element_by_xpath("//*[@id='ADD_BTN']").click()
    try:
        driver.find_element_by_xpath("//div[contains(@class, 'progress-striped')]")
    except:
        logging.getLogger(caseName).info( "Create failed")
    sleep(100)
    driver.refresh()
    
def addMonitor(caseName, driver, ip):
    logging.getLogger(caseName).info( "add Monitor")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_CLUSTERSETTING).click()  
    sleep(5)
    rowCount = len (driver.find_elements_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr")) 
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info(i)
        nodeIp = driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[3]"%(i)).text
        logging.getLogger(caseName).info( nodeIp)        
        if(nodeIp.replace(' ','') ==ip):
            try:
                if(driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[4]"%(i)).text.replace(' ','') == 'False'):
                    driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[5]/button[1]"%(i)).click()
                    driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
                    logging.getLogger(caseName).info( "now sleep 100s")
                    sleep(100)
                    driver.refresh()
                else:
                    logging.getLogger(caseName).info( "cannot add the mon")
            except:
                logging.getLogger(caseName).info( "the mon is not shown ")
            return
        sleep(1)   
        
    driver.refresh()     
    return

def deleteMonitor(caseName, driver,ip):
    logging.getLogger(caseName).info( "delete mon")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_CLUSTERSETTING).click()  
    sleep(5)
    rowCount = len (driver.find_elements_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr")) 
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        nodeIp = driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[3]"%(i)).text
        logging.getLogger(caseName).info( nodeIp)
        if(nodeIp.replace(' ','') ==ip):
            try:
                if(driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[4]"%(i)).text.replace(' ','') == 'Up'):
                    driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[5]/button[2]"%(i)).click()
                    driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
                    logging.getLogger(caseName).info( "now sleep 100s")
                    sleep(100)
                    driver.refresh()
                else:
                    logging.getLogger(caseName).info( "cannot delete the mon")
            except:
                logging.getLogger(caseName).info( "the mon is not shown ")
        sleep(1) 
    driver.refresh()       
    return
         
def deleteNode(caseName, driver,ip):
    logging.getLogger(caseName).info( "delete nodes")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_CLUSTERSETTING).click()
    sleep(5)
    rowCount = len (driver.find_elements_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr")) 
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        nodeIp = driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[3]"%(i)).text
        logging.getLogger(caseName).info( nodeIp)
        if(nodeIp.replace(' ','') ==ip):
            try:
                if(driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[5]/button[3]"%(i)).is_displayed()):
                    driver.find_element_by_xpath("//table[@id='SERVER_LIST_TABLE']/tbody/tr[%s]/td[5]/button[3]"%(i)).click()
                    driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
                    logging.getLogger(caseName).info( "now sleep 100s")
                    sleep(100)
                    driver.refresh()
                else:
                    logging.getLogger(caseName).info( "cannot delete the node")
                    return
            except:
                logging.getLogger(caseName).info( "the node cannot be deleted")
        sleep(1)   
    driver.refresh()     
    return
'''
input parameter:
    - driver
    - preTimeNum
    - preTimeUnit
    - fromTime
    - toTime
    - source
    - service
    - level
    - eventType
    - operation
'''
def filterEventLog(caseName, driver, preTimeNum="", preTimeUnit="", fromTime="", toTime="", source="", service="", level="", eventType="", operation="filter"):
    logging.getLogger(caseName).info( "filter event logs")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_EVENTLOGS).click()    
    sleep(2)
    driver.find_element_by_xpath("//button[@id='id-filter-group-btn']").click() 
    #PreTime to Now Model
    if(preTimeNum ):
        driver.find_element_by_xpath("//input[@id='TIME_DISCRETE']").click() 
        driver.find_element_by_xpath("//input[@id='FILTER_TIME_DISCRETE_INPUT']").send_keys(preTimeNum)
        try:
            driver.find_element_by_xpath("//span[contains(@class, 'ist-error-icon')]")
            logging.getLogger(caseName).info( "The name for snap is illegal ")
            return
        except:
            logging.getLogger(caseName).info( "element for from tim is right")
            #driver.find_element_by_xpath("//li[contains(text(), preTimeUnit)]").click()
            if(preTimeUnit):
                sleep(2)
                driver.find_element_by_xpath("//div/button[@id='DISCREET_TIME_DROPDOWN']").click()   
                rowCount = len (driver.find_elements_by_xpath("//div/ul/li[@id='TIME_OPTIONS']"))
                for i in range(1, rowCount+1):            
                    if(driver.find_element_by_xpath("//div/ul/li[%s][@id='TIME_OPTIONS']"%(i)).text.lower() == preTimeUnit.lower()):
                        driver.find_element_by_xpath("//div/ul/li[%s][@id='TIME_OPTIONS']"%(i)).click()
                        sleep(10)
    #From To Model
    elif(fromTime and toTime):
        driver.find_element_by_xpath("//input[@id='TIME_RANGE']").click() 
        sleep(2) 
        driver.find_element_by_xpath("//input[@id='DATETIME_INPUT1']").send_keys(fromTime)
        driver.find_element_by_xpath("//input[@id='DATETIME_INPUT2']").send_keys(toTime)
        
    if(source):
        driver.find_element_by_xpath("//input[@id='EVENTLOG_ORIGIN']").send_keys(source)
    if(service):
        driver.find_element_by_xpath("//button[@id='SOURCE_DROPDOWN']").click()
        rowCount = len (driver.find_elements_by_xpath("//li[@id='SOURCE']"))
        for i in range(1, rowCount+1):                      
            if(driver.find_element_by_xpath("//li[%s][@id='SOURCE']/span"%(i)).text == service):
                driver.find_element_by_xpath("//li[%s][@id='SOURCE']"%(i)).click()
                sleep(10)
        #selForService = Select(driver.find_element_by_xpath("//button[@id='SOURCE_DROPDOWN']"))
        #selForService.select_by_visible_text(service)
    if(level):
        driver.find_element_by_xpath("//button[@id='SEVERITY_DROPDOWN']").click()
        rowCount = len (driver.find_elements_by_xpath("//div[@id='id-event-filter-body-div']//div[4]//div[@class='ist-form-item-5']//div//ul[@class='dropdown-menu']//li"))
        for i in range(1, rowCount+1):       
            if(driver.find_element_by_xpath("//div[@id='id-event-filter-body-div']//div[4]//div[@class='ist-form-item-5']//div//ul[@class='dropdown-menu']//li[%s]//span"%(i)).text == level):
                driver.find_element_by_xpath("//div[@id='id-event-filter-body-div']//div[4]//div[@class='ist-form-item-5']//div//ul[@class='dropdown-menu']//li[%s]"%(i)).click()
                sleep(10)
                
    if(eventType):
        driver.find_element_by_xpath("//button[@id='EVENT_TYPE_DROPDOWN']").click()
        rowCount = len (driver.find_elements_by_xpath("//li[@id='EVENT_TYPE']"))
        for i in range(1, rowCount+1):   
            if(driver.find_element_by_xpath("//li[%s][@id='EVENT_TYPE']//span"%(i)).text == eventType):
                driver.find_element_by_xpath("//li[%s][@id='EVENT_TYPE']"%(i)).click()
                sleep(10)
    sleep(10)
    if(operation=="filter"):
        if(driver.find_element_by_xpath("//div/button[@id='FILTER_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/button[@id='FILTER_BTN']").click()  
    if(operation=="reset"):  
        if(driver.find_element_by_xpath("//div/a[@id='RESET_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/a[@id='RESET_BTN']").click()  
    if(operation=="cancel"): 
        if(driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").click()          
    return
'''
input parameter:
    - driver
    - logType
    - preTimeNum
    - preTimeUnit
    - fromTime
    - toTime
    - operation
'''
def exportEventLog(caseName, driver, logType='event', preTimeNum="", preTimeUnit="", fromTime="", toTime="", operation="export"):
    logging.getLogger(caseName).info( "export event logs")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_EVENTLOGS).click() 
    driver.find_element_by_xpath("//button[@id='events-export-btn']").click()    
    sleep(2)
    if(logType=='event'):
        driver.find_element_by_xpath("//input[@id='REPORT_EVENT_LOG']").click() 
    if(logType=='audit'):
        driver.find_element_by_xpath("//input[@id='REPORT_AUDIT_LOG']").click()  
    sleep(2)
    #preTime mode
    if(preTimeNum ):
        driver.find_element_by_xpath("//input[@id='DISCRETE_GENERATE_REPORT_RADIO']").click() 
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_DISCRETE_VALUE']").send_keys(preTimeNum)
        try:
            driver.find_element_by_xpath("//span[contains(@class, 'ist-error-icon')]")
            logging.getLogger(caseName).info( "The name for snap is illegal ")
            return
        except:
            logging.getLogger(caseName).info( "element for from tim is right")
            #driver.find_element_by_xpath("//li[contains(text(), preTimeUnit)]").click()
            if(preTimeUnit):
                sleep(2)
                driver.find_element_by_xpath("//div/button[@id='DISCREET_UNIT_DROPDOWN']").click()   
                rowCount = len (driver.find_elements_by_xpath("//div/ul/li[@id='OPTION']"))
                for i in range(1, rowCount+1):            
                    if(driver.find_element_by_xpath("//div/ul/li[%s][@id='OPTION']"%(i)).text.lower() == preTimeUnit.lower()):
                        driver.find_element_by_xpath("//div/ul/li[%s][@id='OPTION']"%(i)).click()
                        sleep(10)
    #From To Model
    elif(fromTime and toTime):
        driver.find_element_by_xpath("//input[@id='RANGE_GENERATE_REPORT_RADIO']").click()
        sleep(2) 
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_RANGE_FROMDATE']").click()
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_RANGE_FROMDATE']").send_keys(fromTime)
        sleep(2)
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_RANGE_TODATE']").click()
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_RANGE_TODATE']").send_keys(toTime)
        sleep(3)
        driver.find_element_by_xpath("//input[@id='PREV_REPORT_RANGE_FROMDATE']").click()
    sleep(5)    
    if(operation =='export'):
        if(driver.find_element_by_xpath("//div/button[@id='OK_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/button[@id='OK_BTN']").click()  
    if(operation == 'cancel'):
        if(driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").click() 
    driver.refresh() 
    return
'''
input parameter:
    - driver
    - preTimeNum
    - preTimeUnit
    - fromTime
    - toTime
    - firstName
    - lastName
    - userType
    - logInAddress
    - operation
'''
def filterAuditLog(caseName, driver, preTimeNum="", preTimeUnit="", fromTime="", toTime="", firstName="", lastName="", userType="",logInAddress="", operation="filter"):
    logging.getLogger(caseName).info( "filter audit logs")
    driver.find_element_by_id(element.GOTO_CLUSTERMGMT).click() 
    driver.find_element_by_id(element.GOTO_EVENTLOGS).click() 
    driver.find_element_by_id(element.AUDIT_LOGS_BTN).click() 
    sleep(2)
    driver.find_element_by_xpath("//button[@id='FILTER_DROPDOWN']").click() 
    #PreTime to Now Model
    if(preTimeNum ):
        driver.find_element_by_xpath("//input[@id='TIME_DISCRETE']").click() 
        driver.find_element_by_xpath("//input[@id='FILTER_TIME_DISCRETE_VALUE']").send_keys(preTimeNum)
        try:
            driver.find_element_by_xpath("//span[contains(@class, 'ist-error-icon')]")
            logging.getLogger(caseName).info( "The name for snap is illegal ")
            return
        except:
            logging.getLogger(caseName).info( "element for from tim is right")
            #driver.find_element_by_xpath("//li[contains(text(), preTimeUnit)]").click()
            if(preTimeUnit):
                sleep(2)
                driver.find_element_by_xpath("//div/button[@id='DISCREET_UNIT_DROPDOWN']").click()   
                rowCount = len (driver.find_elements_by_xpath("//div/ul/li[@id='TIME_OPTION']"))
                for i in range(1, rowCount+1):            
                    if(driver.find_element_by_xpath("//div/ul/li[%s][@id='TIME_OPTION']"%(i)).text.lower() == preTimeUnit.lower()):
                        driver.find_element_by_xpath("//div/ul/li[%s][@id='TIME_OPTION']"%(i)).click()
                        sleep(10)
    #From To Model
    elif(fromTime and toTime):
        driver.find_element_by_xpath("//input[@id='TIME_RANGE']").click() 
        sleep(2) 
        driver.find_element_by_xpath("//input[@id='FILTER_TIME_RANGE_FROMDATE']").send_keys(fromTime)
        driver.find_element_by_xpath("//input[@id='FILTER_TIME_RANGE_TODATE']").send_keys(toTime)
    #input first name and last name
    if(firstName and lastName):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_FIRSTNAME']").send_keys(firstName)
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_LASTNAME']").send_keys(lastName)  
    
    #input user type
    if(userType):
        driver.find_element_by_xpath("//button[@id='GROUPLIST_DROPDOWN']").click()
        rowCount = len (driver.find_elements_by_xpath("//li[@id='GROUP']"))
        logging.getLogger(caseName).info( rowCount )
        for i in range(1, rowCount+1): 
            logging.getLogger(caseName).info( driver.find_element_by_xpath("//li[%s][@id='GROUP']//span"%(i)).text)     
            if(driver.find_element_by_xpath("//li[%s][@id='GROUP']//span"%(i)).text == userType):
                driver.find_element_by_xpath("//li[%s][@id='GROUP']"%(i)).click()
                sleep(10)
    if(logInAddress) :           
        driver.find_element_by_xpath("//input[@id='EVENTLOG_USER_ADDRESS']").send_keys(logInAddress)  
    
    if(operation=="filter"):
        if(driver.find_element_by_xpath("//div/button[@id='FILTER_DTM']").is_displayed()):
            driver.find_element_by_xpath("//div/button[@id='FILTER_DTM']").click()  
    if(operation=="reset"):  
        if(driver.find_element_by_xpath("//div/a[@id='RESET_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/a[@id='RESET_BTN']").click()  
    if(operation=="cancel"): 
        if(driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").is_displayed()):
            driver.find_element_by_xpath("//div/a[@id='CANCEL_BTN']").click()          
    return

if __name__=="__main__":
    
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    
    ip1="192.168.29.5"
    addIp = '192.168.29.36'
    port="3579"
    url =  "http://"+ip1+":"+port
    driver.get(url)
    loginlogout.login(driver, ip1,port)
    loginlogout.changeEnglish(driver)
    #poolManagement.createPool(driver,poolName, poolCapcity)
    #addNode(driver,addIp)
    #addMonitor(driver,addIp)
    #deleteMonitor(driver,addIp)
    #deleteNode(driver,addIp)
    #filterEventLog(driver,  fromTime="06/20/2017 11:00 AM", toTime="06/21/2017 12:00 AM", source='denali1', service="NodeJS", level="Low", eventType="cpu-average")
    #filterAuditLog(driver,  fromTime="06/20/2017 11:00 AM", toTime="06/21/2017 12:00 AM", firstName="admin", lastName="admin", userType="Master Administrator",logInAddress="192.168.24.107 ", operation="filter")
    exportEventLog(driver,  fromTime="2017-06-21", toTime="2017-06-22")
    #exportEventLog(driver, preTimeNum="2", preTimeUnit="Days")
    #logging.getLogger(caseName).info( "case complete")