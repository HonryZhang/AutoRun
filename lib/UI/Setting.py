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

#For systemsetting->UI settings
def UISetting(caseName, driver, color='blue', logoImagePath="", operation='save'):
    logging.getLogger(caseName).info("UI setting")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id("GOTO_SYSTEMSETUP").click() 
    sleep(1)
    driver.find_element_by_xpath("//a[@id='control_setting_link']").click() 
    #change color
    driver.find_element_by_xpath("//button[@id='ist_theme_btn']").click()
    rowCount = len (driver.find_elements_by_xpath("//li[contains(@id,'ist_theme_option_li')]"))
    logging.getLogger(caseName).info(rowCount)
    for i in range(1, rowCount+1): 
        logging.getLogger(caseName).info(driver.find_element_by_xpath("//li[%s][contains(@id,'ist_theme_option_li')]//span"%(i)).text)     
        if(driver.find_element_by_xpath("//li[%s][contains(@id,'ist_theme_option_li')]//span"%(i)).text.lower()  == color.lower()):
            driver.find_element_by_xpath("//li[%s][contains(@id,'ist_theme_option_li')]"%(i)).click()
            sleep(10)
    #upload picture
    '''
    if(logoImagePath):
        logging.getLogger(caseName).info(len(driver.find_elements_by_xpath("//*[@id='ist_logo_btn']"))
        driver.find_element_by_xpath("//*[@id='ist_logo_btn']").click()
        driver.find_element_by_xpath("//input[@id='ist_logo_path_input']").send_keys(logoImagePath)
        sleep(6)
    '''
    if(operation=='save') :
        driver.find_element_by_xpath("//button[@id='ist_save_btn']").click()  
    if(operation=='cancel'):
        driver.find_element_by_xpath("//a[@id='ist_cancel_link']").click() 
    driver.refresh()

#For systemsetting->Email settings
def emailSetting(caseName, driver, enable="1", smtpAddress="", smtpRelayPort="", enableSmtpAuth="1", userName="", passwd="",enableSenderAddress="", subject="", notification="", operation="save"):       
    logging.getLogger(caseName).info("email setting")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id("GOTO_SYSTEMSETUP").click() 
    sleep(1) 
    driver.find_element_by_xpath("//a[@id='email_setting_link']").click()
    try:           
        checkbox=driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_ENABLE']")
        if (checkbox.is_selected() and enable =='0'):
            logging.getLogger(caseName).info("checkbox is selected..now please deselected")
            checkbox.click()
        elif(not checkbox.is_selected() and enable=='1'):            
            print("radio is not selected...now please selected")
            checkbox.click()
            if(smtpAddress):
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_ADDRESS']").clear()
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_ADDRESS']").send_keys(smtpAddress)
            if(smtpRelayPort):
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_PORT']").clear()
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_PORT']").send_keys(smtpRelayPort)            
            if(enableSmtpAuth=="1"):
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_AUTH']").click()  
                if(userName and passwd):
                    driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_USERNAME']").clear()
                    driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_USERNAME']").send_keys(userName)
                    driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_PASSWORD']").clear()
                    driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SMTP_PASSWORD']").send_keys(passwd)
            if(enableSenderAddress):
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_COMPOSE_FROM']").clear()
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_COMPOSE_FROM']").send_keys(enableSenderAddress)  
            if(subject):
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SUBJECT']").clear()
                driver.find_element_by_xpath("//input[@id='CLUSTER_EMAIL_FORM_SUBJECT']").send_keys(subject)        
            if(notification) :
                driver.find_element_by_xpath("//button[@id='CLUSTER_EMAIL_FORM_NOTIFICATIONS']").click()
                if(notification == 'Batch All'):
                    logging.getLogger(caseName).info(notification)
                    sleep(1)
                    driver.find_element_by_xpath("//li[@id='NOTIFYTYPE_ALL']").click()  
            sleep(5)

            errElements=driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
            if(len(errElements)>0):
                logging.getLogger(caseName).info("some parameter is wrong, check again" )
                return             
            sleep(1)      
            if( operation=="save"):
                logging.getLogger(caseName).info("now save the values")
                driver.find_element_by_xpath("//button[@id='SAVE_BTN']").click()
            if(operation=="cancel"):
                driver.find_element_by_xpath("//a[@id='ist_cancel_link']").click()            
    except Exception as e:
        logging.getLogger(caseName).info("Exception occured", format(e))
    finally:
        driver.quit()
        logging.getLogger(caseName).info("case complete")    
    return

#For User setting->General
def setGeneralTimeout(caseName, driver, timeNum='60', timeUnit='Minutes'):
    logging.getLogger(caseName).info("set GeneralTimeout")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id(element.GOTO_USERMANAGEMENT).click() 
    sleep(1)
    driver.find_element_by_xpath("//a[@id='id-usergroup-setting']").click() 
    sleep(1)
    driver.find_element_by_xpath("//input[@id='control_timeout_input']").clear()
    driver.find_element_by_xpath("//input[@id='control_timeout_input']").send_keys(timeNum)
    driver.find_element_by_xpath("//div/button[@id='ist_timeout_unit_btn']").click()   
    rowCount = len (driver.find_elements_by_xpath("//div/ul/li[contains(@id, 'ist_timeout_unit_li')]"))
    for i in range(1, rowCount+1):            
        if(driver.find_element_by_xpath("//div/ul/li[%s][contains(@id, 'ist_timeout_unit_li')]"%(i)).text.lower() == timeUnit.lower()):
            driver.find_element_by_xpath("//div/ul/li[%s][contains(@id, 'ist_timeout_unit_li')]"%(i)).click()
    sleep(2)
    if(driver.find_element_by_xpath("//div/button[@id='ist_save_btn']").is_displayed()):
        driver.find_element_by_xpath("//div/button[@id='ist_save_btn']").click()

    return

def addUser(caseName, driver,username="", passwd="", email="", receiveAlertEmail='1', firstName="", lastName="", auth="", operation='create'):
    logging.getLogger(caseName).info("add user")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id(element.GOTO_USERMANAGEMENT).click() 
    sleep(1)
    driver.find_element_by_xpath("//a[@id='id-user-list']").click()
    sleep(2)
    driver.find_element_by_xpath("//button[@id='user-create-btn']").click()
    sleep(1)
    if(username):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_ID']").send_keys(username)
    if(passwd):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_PASSWORD']").send_keys(passwd)
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_CONFIRMPASSWORD']").send_keys(passwd)
    if(email):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_EMAIL']").send_keys(email)
    if(receiveAlertEmail):
        driver.find_element_by_xpath("//input[@id='ENABLE_NOTIFICATION']").click()
    if(firstName):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_FIRSTNAME']").send_keys(firstName)
    if(lastName):
        driver.find_element_by_xpath("//input[@id='USER_MANAGEMENT_EDIT_FORM_LASTNAME']").send_keys(lastName)
    driver.find_element_by_xpath("//div/button[@id='USER_GROUP_AUTH']").click()   
    rowCount = len (driver.find_elements_by_xpath("//div/ul/li[contains(@id, 'USER_GROUP')]"))
    for i in range(1, rowCount+1):            
        if(driver.find_element_by_xpath("//div/ul/li[%s][contains(@id, 'USER_GROUP')]"%(i)).text.lower() == auth.lower()):
            driver.find_element_by_xpath("//div/ul/li[%s][contains(@id, 'USER_GROUP')]"%(i)).click()
    sleep(2)
    if(operation=='create'):
        driver.find_element_by_xpath("//button[@id='OK_BTN']").click()
    if(operation=='cancel'):
        driver.find_element_by_xpath("//a[@id='CANCEL_BTN']").click()  
    sleep(10)
    driver.refresh()  
    return

def delUser(caseName, driver,username=""):
    logging.getLogger(caseName).info("delete user")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id(element.GOTO_USERMANAGEMENT).click() 
    sleep(1)
    driver.find_element_by_xpath("//a[@id='id-user-list']").click()
    sleep(5)
    rowCount = len (driver.find_elements_by_xpath("//table[@id='USER_MANAGEMENT_USER_LIST_TABLE']//tbody//tr"))
    logging.getLogger(caseName).info(rowCount)
    #//*[@id="DELETE_USER_BTN-0"]
    delElements = driver.find_elements_by_xpath("//button[contains(@id, 'DELETE_USER_BTN')]")
    logging.getLogger(caseName).info(len(delElements))
    for i in range(1, rowCount+1):  #/html/body/div[2]/div/div/div/div/div[2]/form/div/div[2]/div/div[2]/div/table/tbody/tr/td[8]/button[2]
        logging.getLogger(caseName).info(driver.find_element_by_xpath("//table[@id='USER_MANAGEMENT_USER_LIST_TABLE']//tbody//tr[%s]//td[3]"%(i)).text.replace(" ",""))  
        if(driver.find_element_by_xpath("//table[@id='USER_MANAGEMENT_USER_LIST_TABLE']//tbody//tr[%s]//td[3]"%(i)).text.replace(" ","") == username):
            driver.find_element_by_xpath("//table[@id='USER_MANAGEMENT_USER_LIST_TABLE']//tbody//tr[%s]//td[8]//button[2]"%(i)).click()
            #delElements[i].click()
            driver.find_element_by_xpath("//a[@id='OK_BTN']").click()    
    sleep(5)
    driver.refresh()    
 
def enableLDAP(caseName, driver, enabled='1', host='',port='', ssl='', bindDN='', bindDNpasswd='', baseDN='', userID='', searchCon='', firstName='', lastName='', userEmail='', operation='save'):  
    logging.getLogger(caseName).info("enable the LDAP")
    driver.find_element_by_id(element.GOTO_SYSTEMSETTING).click() 
    sleep(1)
    driver.find_element_by_id(element.GOTO_USERMANAGEMENT).click() 
    sleep(5)
    driver.find_element_by_xpath("//a[@id='id-user-ldap-setting']").click()
    sleep(1)
    checkbox=driver.find_element_by_xpath("//input[@id='ENABLE_LDAP_CHECKBOX']")
    if (checkbox.is_selected() and enabled =='0'):
        logging.getLogger(caseName).info("checkbox is selected..now please deselected")
        checkbox.click()
        if(driver.find_element_by_xpath("//button[@id='SAVE_BTN']").is_displayed()):
            driver.find_element_by_xpath("//button[@id='SAVE_BTN']").click()
    if(not checkbox.is_selected() and enabled =='1'):
        logging.getLogger(caseName).info("checkbox is not selected..now please selected")
        checkbox.click()
    if(enabled =='0')  :
        return  
    if(enabled =='1'):
        if(host):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_HOSTNAME']").send_keys(host)
        if(port):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_PORT']").send_keys(port)
        if(ssl):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_SSL']").click()
        if(bindDN):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_BINDDN']").send_keys(bindDN)
        if(bindDNpasswd):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_BINDPASSWORD']").send_keys(bindDNpasswd)
        if(baseDN):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_BASEDN']").send_keys(baseDN)
        if(userID):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_USERFIELD']").send_keys(userID)
        if(searchCon):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_USER_FILTER_FIELD']").send_keys(searchCon)
        if(firstName):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_USER_FIRSTNAME_FIELD']").send_keys(firstName)
        if(lastName):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_USER_LASTNAME_FIELD']").send_keys(lastName)
        if(userEmail):
            driver.find_element_by_xpath("//input[@id='UMAN_LDAP_USER_EMAIL_FIELD']").send_keys(userEmail)
  
        if(operation == 'save'):
            if(driver.find_element_by_xpath("//button[@id='SAVE_BTN']").is_displayed()):
                driver.find_element_by_xpath("//button[@id='SAVE_BTN']").click()
                sleep(5)
        if(operation == 'cancel'):
            driver.find_element_by_xpath("//a[@id='ist_cancel_link']").click()
        errElements=driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        if(len(errElements)>0):
            logging.getLogger(caseName).info("some parameter is wrong, check again") 
            return
    return     

'''                        
if __name__=="__main__":
    from lib.UI import loginlogout
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    #driver = webdriver.Chrome(chromedriver)
    options = webdriver.ChromeOptions()
    prefs = {"":""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    ip1="192.168.29.5"
    addIp = '192.168.29.36'
    port="3579"
    url =  "http://"+ip1+":"+port
    driver.get(url)
    driver.maximize_window()
    sleep(2)
    loginlogout.login(driver, ip1,port)
    loginlogout.changeEnglish(driver)
    logoImagePath='E:\\login_error_2.PNG'
    #UISetting(driver, color='Java', logoImagePath= logoImagePath)
    #emailSetting(driver, enable="1", smtpAddress="smtp.office365.com", smtpRelayPort="587", enableSmtpAuth="1", userName="lin", passwd="li",enableSenderAddress="from_address@istuary.com", subject="event notification", notification="Batch All", operation="save")
    #setGeneralTimeout(driver, timeNum='60', timeUnit='hours')
    #addUser(driver,username="abc", passwd="123456", email="abd@qq.com", receiveAlertEmail='1', firstName="abc", lastName="cba", auth="No Access", operation='create')
    #delUser(driver,username="abc")
    enableLDAP(driver, enabled='1', host='10.0.10.42',port='389', ssl='1', bindDN='CN=qa_bind,OU=LDAP,OU=Istuary,DC=istuary,DC=co', bindDNpasswd='ist.1234', baseDN='OU=Istuary,DC=istuary,DC=co', userID='sAMAccountName', searchCon='(&(objectCategory=Person)(objectClass=person))', firstName='givenName', lastName='sn', userEmail='mail', operation='save')
    '''  