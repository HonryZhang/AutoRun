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

def login(caseName, driver, ip1, port, userName, passwd):
    driver.implicitly_wait(3)
    logging.getLogger(caseName).info( "login")
    sleep(5)
    driver.find_element_by_id(element.USERNAME_INPUT).send_keys(userName)
    driver.find_element_by_id(element.PASSWORD_INPUT).send_keys(passwd)
    driver.implicitly_wait(0.5)
    driver.find_element_by_id("login-button").click()
    sleep(1)
    try:
        if(driver.find_element_by_id("login-error-msg").is_displayed()):
            logging.getLogger(caseName).info("invalide user name or passwd is found")
    except:
        logging.getLogger(caseName).info("now we have loggin")
    return   

def changeEnglish(driver):
    driver.find_element_by_xpath("//button[@id='SWITCH_LANG']").click()
    return

def logout(caseName, driver):    
    logging.getLogger(caseName).info( "logout")
    driver.implicitly_wait(3)
    driver.find_element_by_id("unique-dropdown").click()
    #ActionChains(driver).move_to_element(logoutId).click()
    sleep(1)
    driver.find_element_by_id("LOGOUT_BTN").click()
    
def accountSetting(caseName, driver, firstName="", lastName="", currentPasswd="", newPasswd="", confirmPasswd="", email="", receiveAlertEmail=""):
    logging.getLogger(caseName).info( "Go to account settings")
    sleep(10)    
    element = driver.find_element_by_xpath("//*[@id='unique-dropdown']/h5")
    ActionChains(driver).move_to_element(element).perform();
    logging.getLogger(caseName).info( element.text)
    element.click()
    driver.find_element_by_id(element.GOTO_ACCOUNTSETTINGS).click()  
    if(firstName):
        driver.find_element_by_id("MY_ACCOUNT_USERFIRSTNAME_en").clear()
        driver.find_element_by_id("MY_ACCOUNT_USERFIRSTNAME_en").send_keys(firstName)
    if(lastName):
        driver.find_element_by_id("MY_ACCOUNT_USERLASTNAME").clear()
        driver.find_element_by_id("MY_ACCOUNT_USERLASTNAME").send_keys(lastName)
    if(currentPasswd):
        driver.find_element_by_id("CURR_PASSWORD_INPUT").send_keys(currentPasswd)
    if(confirmPasswd):
        driver.find_element_by_id("NEW_PASSWORD_INPUT").send_keys(confirmPasswd)
    if(email):
        driver.find_element_by_id("MY_ACCOUNT_EMAIL").send_keys(email)
    if(receiveAlertEmail):
        driver.find_element_by_id("//label[@for='ENABLE_NOTIFICATION']").click()
    sleep(2)
    driver.find_element_by_id("SAVE_BTN").click()
    sleep(2)
    driver.refresh()
    return

def changeProfilePhoto(caseName, driver):
    logging.getLogger(caseName).info( "Change profile photo")  
    driver.implicitly_wait(3)
    driver.find_element_by_id("unique-dropdown").click()
    driver.find_element_by_id(element.GOTO_ACCOUNTSETTINGS).click()  
    driver.implicitly_wait(3)
    changeImg = driver.find_element_by_xpath("//div[@class='user-img-container']//img[1]")
    ActionChains(driver).move_to_element(changeImg).perform()
    driver.find_element_by_xpath("//div[@class='user-img-container']//button[1]").click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//img[@src='app/resources/default/images/profilePhoto/2.jpg']").click()
    sleep(1)
    driver.find_element_by_id("USE_PHOTO_BTN").click()
    sleep(1)
    driver.find_element_by_id("SAVE_BTN").click()
    sleep(2)
    driver.refresh()

if __name__=="__main__":
    
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
    login(driver, ip1,port)
    changeEnglish(driver)
    accountSetting(driver,firstName="admin", lastName="admin" )
    #logging.getLogger(caseName).info( "case complete"