from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time 
import os
import urllib
import re
import sys
import getopt
import commands
import pexpect
#from lib.UI import *

port="3579"
license1="test"
license2="test"
license3="test"
ipNodeList="192.168.29.5, 192.168.29.6, 192.168.29.7"
publicNetwork="192.168.28.0/23"
clusterNetwork="192.168.28.0/23"
help  = False
caseDescription='''
init the cluster from UI
'''

def getOpts():
    global ipNodeList
    global publicNetwork
    global clusterNetwork
    global help
    options, remainder = getopt.getopt(sys.argv[1:], 'i:p:c:h', ['ipNodeList=', 
                                                     'publicNetwork=',
                                                     'clusterNetwork=',
                                                     'help',
                                                     ])
    for opt, arg in options:
        if opt in ('-i', '--ipNodeList'):
            ipNodeList = arg
        elif opt in ('-p','--publicNetwork'):
            publicNetwork = arg
        elif opt in ('-c','--clusterNetwork'):
            clusterNetwork = arg
        elif opt in ('-h','--help'):
            help = True
    print help
    if(len(ipNodeList) == 0 and len(publicNetwork) == 0 and len(clusterNetwork) == 0) and (not help):
        print "We will use following information to reinit the cluser"
        print "ipNodelist: 192.168.29.5, 192.168.29.6, 192.168.29.7"
        print "publicNetwork: 192.168.28.0/24"
        print "clusterNetwork: 192.168.28.0/24"
    if(help):
        print "Welcome to use this tool to install and initialize the cluster environment"
        print "-i: ipNodeList, node ip list"
        print "-p: publicNetwork, the public network"
        print "-c: clusterNetwork, the cluster network"
        exit()
        

def main():
    print caseDescription
    #chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    #os.environ["webdriver.chrome.driver"] = chromedriver
    #driver = webdriver.Chrome(chromedriver)
    options = webdriver.ChromeOptions()
    prefs = {"":""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    options.add_experimental_option("prefs", prefs)

    ipList = ipNodeList.split(",")
    ip1 = ipList[0]
    ip2 = ipList[1]
    ip3 = ipList[2]
    print ip1
    print ip2
    print ip3  
   
    driver = webdriver.Chrome(chrome_options=options)
    
    url =  "http://"+ip1+":"+port
    #userName= nodeList[0].getUserName()
    #passwd=nodeList[0].getPassword()
    driver.get(url)
    
    driver.implicitly_wait(3)
    time.sleep(1)
    driver.find_element_by_id("INITIALIZE_START_CLICK").click()
    driver.implicitly_wait(0.5)
    name=driver.find_element_by_id("CLUSTER_NAME_INPUT").send_keys("UITestCluster")
    driver.implicitly_wait(0.5)
    driver.find_element_by_id("ADMIN_LASTNAME_INPUT_Zh_Mode").send_keys("admin")
    driver.find_element_by_id("ADMIN_FIRSTNAME_INPUT").send_keys("admin")
    driver.find_element_by_id("ADMIN_EMAIL_INPUT").send_keys("mm@a.com")
    driver.find_element_by_id("INITIALIZE_ADMIN_NEXT_BTN").click()
    driver.implicitly_wait(0.5)
    driver.find_element_by_id("INITIALIZE_BLOCK_STORAGE_TYPE").click()
    time.sleep(0.5)
    driver.find_element_by_id("INITIALIZE_TYPE_NEXT_BTN").click()
    driver.implicitly_wait(0.5)
    time.sleep(1)
    #driver.find_element_by_id("111").send_keys("192.168.28.59")
    driver.find_element_by_id("INITIALIZE_IP_ADDRESS_INPUT1").send_keys(ip2)
    driver.find_element_by_id("INITIALIZE_IP_ADDRESS_INPUT2").send_keys(ip3)
    driver.find_element_by_id("INITIALIZE_IP_NEXT_BTN").click()
    driver.implicitly_wait(0.5)
    time.sleep(1)
    
    driver.find_element_by_id("LICENSE-0").send_keys(license1)
    driver.find_element_by_id("LICENSE-1").send_keys(license2)
    driver.find_element_by_id("LICENSE-2").send_keys(license3)
    driver.find_element_by_id("INITIALIZE_LICENSE_NEXT_BTN").click()
    driver.implicitly_wait(0.5)
    time.sleep(2)
    
    driver.find_element_by_xpath('//section[@wz-title="PublicNetwork"]/div/div/div/input').send_keys(publicNetwork)
    driver.find_element_by_xpath("//input[@id='INITIALIZE_PUBLIC_NETWORK_INPUT']").send_keys(clusterNetwork)
    try:
        driver.find_element_by_id("INITIALIZE_PUBLIC_NETWORK_NEXT_BTN").click()
    except:
        time.sleep(10)
        driver.find_element_by_id("INITIALIZE_PUBLIC_NETWORK_NEXT_BTN").click()
    time.sleep(4)
       
    try:
        driver.find_element_by_id("INITIALIZE_REGION_DROPDOWN_BTN").click()
    except:
        time.sleep(2)
        driver.find_element_by_id("INITIALIZE_REGION_DROPDOWN_BTN").click()
    time.sleep(0.5)
    try:
        driver.find_element_by_id("INITIALIZE_REGION_3").click()
    except:
        time.sleep(2)
        driver.find_element_by_id("INITIALIZE_REGION_DROPDOWN_BTN").click()
    time.sleep(0.5)
    try:
        
        driver.find_element_by_id("INITIALIZE_CITY_DROPDOWN_BTN").click()
    except:
        time.sleep(2)
        driver.find_element_by_id("INITIALIZE_CITY_DROPDOWN_BTN").click()
    t1=driver.find_element_by_id("INITIALIZE_CITY_DROPDOWN_BTN")
    ActionChains(driver).click_and_hold(t1).perform()
    
    driver.find_element_by_xpath("//span[contains(text(), 'Shanghai')]").click()
   
    driver.find_element_by_id("INITIALIZE_REGION_NEXT_BTN").click()
    driver.find_element_by_id("INITIALIZE_SUMMARY_NEXT").click()
    driver.find_element_by_xpath("//h1").is_displayed()

    timeout=600
    while timeout:
        status=driver.find_element_by_xpath("//div/h1").text#
        percent=driver.find_element_by_xpath('//h2[@class="currentPercentage ist-text-center ng-binding"]').text#unicode: 65%
        if not percent:
            if driver.find_element_by_id("INITIALIZE_LOGIN_BTN").is_displayed():
                print "complete,status:","complete"
                flag=False
                return
        else:
            print "percent is %s: sleep 20s!, status:%s"%(percent,status)
            time.sleep(20)
            timeout-=20
            
    time.sleep(100000)
    driver.quit()
  
if __name__=="__main__":    
    getOpts()
    main()