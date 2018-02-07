from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re
#driver=webdriver.Firefox()
global url
import element

def goToDashboard(caseName, driver):
    logging.getLogger(caseName).info( "Go to dashboard")
    driver.refresh()
    driver.find_element_by_id("id-menu-dashboard-btn").click()
'''
def goToClusterJoinNodes(caseName, driver):
    logging.getLogger(caseName).info( "Go to Cluster to join nodes")
    driver.refresh()
    driver.implicitly_wait(3)
    driver.find_element_by_id("GOTO_CLUSTERMGMT").click() 
    driver.find_element_by_xpath("GOTO_CLUSTERSETTING").click()

def goToAccountSettings(caseName, driver):
    logging.getLogger(caseName).info( "Go to account settings")
    driver.refresh()
    driver.implicitly_wait(3)
    driver.find_element_by_id("unique-dropdown").click()
    driver.find_element_by_id("GOTO_ACCOUNTSETTINGS").click()  
 
#can only run on chrome
def changeProfilePhoto(caseName, driver):
    logging.getLogger(caseName).info( "Change profile photo" )  
    driver.refresh()
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
    driver.refresh()
'''
def createPool(caseName, driver,poolName, poolCapcity, poolUnit='GB', replicaSize='2'):
    logging.getLogger(caseName).info( "Create pool" )
    #id=element.GOTO_STORAGEPOOLS
    driver.refresh()
    sleep(2)  
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    sleep(1)
    driver.find_element_by_id(element.GOTO_POOLMANAGEMENT).click()
    sleep(1)
    driver.find_element_by_id("storage-pool-create-btn").click()
   
    try:
        driver.find_element_by_id("CREATE_STORAGE_POOL_SIZE").send_keys(poolCapcity) 
    except:
        sleep(2)
        driver.find_element_by_id("CREATE_STORAGE_POOL_SIZE").send_keys(poolCapcity) 
    sleep(1)
    driver.find_element_by_id("CREATE_STORAGE_POOL_NAME").send_keys(poolName) 
    sleep(1)
    driver.find_element_by_id("VOL_REPLICA_NUMBER").click()
    sleep(1)
    if(replicaSize == '3'):
        driver.find_element_by_xpath("//div/ul/li[@id='NUM_3']").click()
    else:
        driver.find_element_by_xpath("//div/ul/li[@id='NUM_2']").click()
    sleep(1)
    driver.find_element_by_id("VOL_UNIT_DROPDOWN").click()
    if(poolUnit=='MB'):
        driver.find_element_by_xpath("//*[@id='UNIT_MB']").click()
    if(poolUnit=='GB'):
        driver.find_element_by_xpath("//*[@id='UNIT_GB']").click()
    if(poolUnit=='TB'):
        driver.find_element_by_xpath("//*[@id='UNIT_TB']").click()    
    driver.find_element_by_xpath("//div[@class='ist-form-item-12']//label[@class='ng-binding']").click()
    sleep(2)
    try:
        poolElements=driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        sleep(15)
        if(len(poolElements)>0):
            logging.getLogger(caseName).info( "The info you input for pool is illegal ")
            for elementItem in poolElements:
                logging.getLogger(caseName).info( elementItem.text)
                #driver.close()
                return
    except:
        logging.getLogger(caseName).info( "element for pool info are all right, now start to create pool")
    driver.find_element_by_id("SAVE_BTN").click()
    sleep(1)
    #driver.
    try:
        driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']")
        sleep(20)
    except:
        logging.getLogger(caseName).info( "Create pool failed: no UITestPool founded")
    driver.refresh()
 
def deletePool(caseName, driver, poolName):
    logging.getLogger(caseName).info( "delete pool" ) 
    driver.refresh()
    sleep(5)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    sleep(1)
    driver.find_element_by_id(element.GOTO_POOLMANAGEMENT).click()
 
    sleep(10)
    driver.find_element_by_id("SEARCH_INPUT").send_keys(poolName)
    sleep(10) #//*[@id="ISCSI_STORAGE_POOLS_LIST_TABLE"]/tbody/tr/td[6]/button[2]/span
    driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr[1]/td[6]/button[2]/span").click()
    sleep(10)
    try:
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    except:
        sleep(2)
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    sleep(2)
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info( driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text)
        if(driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==poolName):
            try:
                driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr[%s]/td[6]/button/span"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='ISCSI_STORAGE_POOLS_LIST_TABLE']/tbody/tr[%s]/td[6]/button/span"%(i)).click()
            ele = driver.find_element_by_xpath("//div[contains(@class,'modal-dialog-content')]")
            logging.getLogger(caseName).info(ele.text)
            #len(re.findall(r'eph-osd stop\/waiting',result))==1
            if(len(re.findall(r'There are images',ele.text))==1):
                logging.getLogger(caseName).info("image found on pool, delete pool failed")
                driver.refresh()
                return
            sleep(5)      
            driver.find_element_by_xpath("//a[@id='OK_BTN']").click()
            sleep(2)  
            break
    '''
    sleep(20)
    driver.refresh()
    #ActionChains(driver).move_to_element(deleteBin).click()    
    
def createBlockDeviceImg(caseName, driver, poolName, imgName, imgSize, imgUnit='GB'):
    logging.getLogger(caseName).info( "create block device img " ) 
    driver.refresh()
    sleep(3)
    
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_id(element.GOTO_DEVICELIST).click()
    sleep(2)
    driver.find_element_by_xpath("//button[@id='iscsi-create-btn']").click()
    sleep(10)
    driver.find_element_by_xpath("//form[@name='CreateBlockImageForm']//div[1]//div//div[1]//div[2]//div[1]//span//button").click()
    try:
        #driver.find_element_by_link_text(" "+imgName).click()
        sleep(2)
        poolElements = driver.find_elements_by_xpath("//div[@class='checkBoxContainer']//div//div[@class='acol']//label//span")
        sleep(2)
        for elementItem in poolElements:
            if(elementItem.text.replace(" ", "").find(poolName) == -1):
                logging.getLogger(caseName).info( "No pool found")
            else:
                elementItem.click()
                driver.find_element_by_xpath("//h1[@class='ng-binding']").click() 
                break
    except:
        logging.getLogger(caseName).info( "No pool found")
        sleep(30)
        #driver.close()
        return
    #driver.find_element_by_xpath("//div[contains(@class, 'acol')]").click()    
    sleep(1)
    driver.find_element_by_xpath("//*[@id='CREATE_BLOCKIMAGE_FORM_NAME']").send_keys(imgName)
    
    sleep(1)
    driver.find_element_by_xpath("//*[@id='CREATE_VOLUME_FORM_SIZE']").send_keys(imgSize)
    sleep(1)
    driver.find_element_by_xpath("//*[@id='VOL_UNIT_DROPDOWN']").click()
    if(imgUnit == 'MB'):
        driver.find_element_by_xpath("//*[@id='UNIT_MB']").click()
    if(imgUnit == 'GB'):
        driver.find_element_by_xpath("//*[@id='UNIT_GB']").click()
    if(imgUnit == 'TB'):
        driver.find_element_by_xpath("//*[@id='UNIT_TB']").click()
    try:
        imgElements = driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        if(len(imgElements)>0):
            for elementItem in poolElements:
                logging.getLogger(caseName).info( elementItem.text)
                logging.getLogger(caseName).info( "The info you input for image is illegal ")
                #driver.close()
                return
    except:
        logging.getLogger(caseName).info( "element for image  is right, now start to create image")
    driver.find_element_by_xpath("//*[@id='CREATE_BTN']").click()
    sleep(20)
    try:
        driver.find_element_by_xpath("//*[@id='SUBMIT_BTN']").click()
    except:
        sleep(10)
        driver.find_element_by_xpath("//*[@id='SUBMIT_BTN']").click()
    sleep(10)
    driver.refresh()
    return

def batchCreateBlockDeviceImg(caseName, driver, poolName, imgName, imgSize,imgNum, imgUnit='GB'):
    logging.getLogger(caseName).info( "Create batch block device img " ) 
    driver.refresh()
    sleep(5)    
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_id(element.GOTO_DEVICELIST).click()
    driver.find_element_by_id("iscsi-create-btn").click()
    sleep(10)
    driver.find_element_by_xpath("//span[contains(@class, 'multiSelect')]").click()
    try:
        #driver.find_element_by_link_text(" "+imgName).click()
        poolElements = driver.find_elements_by_xpath("//div[contains(@class, 'acol')]//label//span")
        for elementItem in poolElements:
            if(elementItem.text.replace(" ", "") == poolName):
                elementItem.click()
    except:
        logging.getLogger(caseName).info( "Image create failed")
        sleep(30)
        #driver.close()
        return
    #driver.find_element_by_xpath("//div[contains(@class, 'acol')]").click()
    driver.find_element_by_xpath("//*[@id='CREATE_BLOCKIMAGE_FORM_NAME']").send_keys(imgName)
    driver.find_element_by_xpath("//h1[@class='ng-binding']").click() 
    driver.find_element_by_xpath("//*[@id='CREATE_VOLUME_FORM_SIZE']").send_keys(imgSize)    
    driver.find_element_by_xpath("//*[@id='VOL_UNIT_DROPDOWN']").click()
    if(imgUnit == 'MB'):
        driver.find_element_by_xpath("//*[@id='UNIT_MB']").click()
    if(imgUnit == 'GB'):
        driver.find_element_by_xpath("//*[@id='UNIT_GB']").click()
    if(imgUnit == 'TB'):
        driver.find_element_by_xpath("//*[@id='UNIT_TB']").click()
    try:
        imgElements = driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        if(len(imgElements)>0):
            for elementItem in poolElements:
                logging.getLogger(caseName).info( elementItem.text)
                logging.getLogger(caseName).info( "The info you input for image is illegal ")
                #driver.close()
                return
    except:
        logging.getLogger(caseName).info( "element for image  is right, now start to create image")
    driver.find_element_by_xpath("//label[@for='IS_BATCH_CREATE_POOL']").click()
    driver.find_element_by_xpath("//input[@id='CREATE_IMAGE-BATCH_NUMBER']").send_keys(imgNum)
    driver.find_element_by_xpath("//*[@id='CREATE_BTN']").click()
    sleep(20)
    driver.find_element_by_xpath("//*[@id='SUBMIT_BTN']").click()
    sleep(10)
    driver.refresh()

#To be update   
def deleteBlockDeviceImg(caseName, driver, imgName):
    logging.getLogger(caseName).info( "Delete block device img " ) 
    driver.refresh()
    sleep(5)    
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_id(element.GOTO_DEVICELIST).click()
    sleep(10)
    driver.find_element_by_id("SEARCH_INPUT").send_keys(imgName)
    sleep(10)
    driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[1]/td[8]/button[2]").click()
    sleep(10)
    try:
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    except:
        sleep(2)
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    sleep(2)
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        try:
            image = driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text
        except:
            sleep(4)
            image = driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text
        logging.getLogger(caseName).info(image )
        if(image.replace(' ','') ==imgName):
            tryFlag = 'true'
            while(tryFlag == 'true'):
                try:
                    driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[7]/button[2]/span"%(i)).click()
                    tryFlag = 'false'
                except:
                    sleep(5)

            #logging.getLogger(caseName).info("check delete successfully")
            ele = driver.find_element_by_xpath("//div[contains(@class,'modal-dialog-content')]")
            logging.getLogger(caseName).info(ele.text)
            #len(re.findall(r'eph-osd stop\/waiting',result))==1
            if(len(re.findall(r'There are snapshots or snapshot tasks',ele.text))==1):
                logging.getLogger(caseName).info("snap found on image")
                driver.refresh()
                return
            sleep(5)      
            try:
                driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            except:
                sleep(2)
                driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            sleep(2)
            return
        '''
    driver.refresh()

#To be update 
def batchDeleteBlockDeviceImg(caseName, driver, imgNum):
    logging.getLogger(caseName).info( "Batch delete block device img")
    driver.refresh()
    sleep(5)
    for i in range(int(imgNum)): 
        sleep(1)
        driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
        driver.find_element_by_id(element.GOTO_DEVICELIST).click()
        driver.find_element_by_xpath ("//span[contains(@class,'fa-trash')]").click()
        sleep(2)
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
        driver.refresh()
        #//*[@id="OK_BTN"]
        sleep(20)
    driver.refresh()
    return 


def createBlockDeviceSnap(caseName, driver, imgName, snapName):
    logging.getLogger(caseName).info( "Create snap for block device " ) 
    driver.refresh()
    sleep(5)
    
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    sleep(4)
    try:
        driver.find_element_by_id("iscsi-create-btn").click()
    except:
        sleep(2)  
        driver.find_element_by_id("iscsi-create-btn").click()  
    #select snap
    sleep(5)
    driver.find_element_by_xpath("//div[@class='tab-content']//div[1]//div//div[1]//span/button").click()
    #driver.find_element_by_xpath("//div[contains(@output-model, 'outputImage')]//span[contains(@class, 'multiSelect')]").click()
    try:
        #driver.find_element_by_link_text(" "+imgName).click()
        imgElements = driver.find_elements_by_xpath("//div[contains(@class, 'acol')]//label//span[contains(@class, 'ng-binding')]")
        
        for elementItem in imgElements:
            logging.getLogger(caseName).info(elementItem.text.replace(" ", ""))
            if(elementItem.text.replace(" ", "").find(imgName) == -1 ):
                logging.getLogger(caseName).info("Not the test image")
            else:
                elementItem.click()
                break
    except:
        logging.getLogger(caseName).info( "No image found")
        sleep(30)
        #driver.close()
        return 
    driver.find_element_by_xpath("//h1[@class='ng-binding']").click()
    driver.find_element_by_id("CREATE_SNAPSHOT_FORM_NAME").send_keys(snapName)
    sleep(5)
    try:
        imgElements = driver.find_elements_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        if(len(imgElements)>0):
            for elementItem in imgElements:
                logging.getLogger(caseName).info( elementItem.text)
                logging.getLogger(caseName).info( "The info you input for snap is illegal ")
                #driver.close()
                return
    except:
        logging.getLogger(caseName).info( "element for snap  is right, now start to create image")
    driver.find_element_by_xpath("//h1[@class='ng-binding']").click() 
    driver.find_element_by_xpath("//button[@id='SUBMIT_BTN']").click()    
    sleep(5)
        
    driver.find_element_by_xpath("//button[@id='SUBMIT_BTN']").click()
    sleep(10)
    driver.refresh()
    return

def deleteBlockDeviceSnap(caseName, driver):
    logging.getLogger(caseName).info( "Delete snap for block device " ) 
    driver.refresh()
    sleep(5)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    driver. find_element_by_xpath ("//span[contains(@class,'fa-trash')]").click()
    sleep(2)
    driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    driver.refresh()

#create snap for a clone
def createBlockDeviceCloneSnap(caseName, driver, cloneName, snapName):
    logging.getLogger(caseName).info( "Create snap for clone " ) 
    driver.refresh()
    sleep(5)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    driver.find_element_by_id("iscsi-create-btn").click()
    sleep(10)
    driver.find_element_by_xpath("//div[@class='ng-isolate-scope']//ul/li[2]").click()
    
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        if(driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==cloneName):
            driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[4]/div/input"%(i)).click()
            sleep(2)  
            break          
    driver.find_element_by_id('CREATE_SNAPSHOT_FORM_NAME').send_keys(snapName)
    sleep(1)
    driver.find_element_by_xpath("//button[@id='SUBMIT_BTN']").click()
    sleep(5)
    driver.refresh()
    return

#create clone for a clock device, need to create snap first
def createClone(caseName, driver, snapName, cloneName):
    logging.getLogger(caseName).info( "Create clone for block device " ) 
    driver.refresh()
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    sleep(10)
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    driver.find_element_by_id("SEARCH_INPUT").send_keys(snapName)
    sleep(10)#//*[@id="CEPH_SNAPSHOTS_LIST_TABLE"]/tbody/tr/td[8]/span/button[2]/span
    driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[1]/td[8]/span/button[2]/span").click()
    sleep(10)
    sleep(2)
    driver.find_element_by_xpath("//input[@id='CREATE_SNAPSHOT_FORM_NAME']").send_keys(cloneName)
    driver.find_element_by_xpath("//button[@id='SUBMIT_BTN']").click()
    sleep(2)
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        if(driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==snapName):
            driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[2]"%(i)).click()
            sleep(2)
            driver.find_element_by_xpath("//input[@id='CREATE_SNAPSHOT_FORM_NAME']").send_keys(cloneName)
            driver.find_element_by_xpath("//button[@id='SUBMIT_BTN']").click()
            sleep(2)
    driver.refresh()
    '''
    return

#restore snap for a clock device, need to create snap first
def restoreSnap(caseName, driver, snapName):
    logging.getLogger(caseName).info( "restore snapshot " ) 
    driver.refresh()
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    sleep(10)#//*[@id="SNAP_RESTORE_BTN-0"]/span
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    driver.find_element_by_id("SEARCH_INPUT").send_keys(snapName)
    sleep(10)#//*[@id="SNAP_RESTORE_BTN-0"]/span
    driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[1]/td[8]/span/button[1]/span").click()
    sleep(5)
    try:
        driver.find_element_by_xpath("//a[@id='OK_BTN']").click()
    except:
        sleep(5)
        driver.find_element_by_xpath("//a[@id='OK_BTN']").click()
    logging.getLogger(caseName).info( "sleep 10s to wait restore complete" ) 
    sleep(10)
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        if(driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==snapName):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[1]"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[1]"%(i)).click()
            sleep(2)            
            driver.find_element_by_xpath("//a[@id='OK_BTN']").click()
            sleep(2)
    driver.refresh()
    return
    '''
 
def deleteSnap(caseName, driver, snapName):
    driver.refresh()
    logging.getLogger(caseName).info( "Create clone for block device " )
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    sleep(10)
    driver.find_element_by_id("SEARCH_INPUT").send_keys(snapName)
    sleep(10)
    driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[1]/td[8]/button/span").click()
    sleep(10)
    try:
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    except:
        sleep(2)
        driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    sleep(2)
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        if(driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==snapName):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[3]"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[3]"%(i)).click()
            sleep(2)   
            ele = driver.find_element_by_xpath("//div[contains(@class,'modal-dialog-content')]")
            logging.getLogger(caseName).info(ele.text)
            #len(re.findall(r'eph-osd stop\/waiting',result))==1
            if(len(re.findall(r'There are ',ele.text))==1):
                logging.getLogger(caseName).info("clone found on snap")
                driver.refresh()
                return         
            driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            sleep(2)
            return
    '''
#flatten clone out then the clone can be operated                    
def flattenBlockDeviceClone(caseName, driver, cloneName):
    driver.refresh()
    logging.getLogger(caseName).info( "flatten clone for block device " )
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/clone']").click()
    sleep(10)
    driver.find_element_by_id("SEARCH_INPUT").send_keys(cloneName)
    sleep(10)
    driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[1]/td[6]/button[1]/span").click()
    sleep(10)
    driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
    '''
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info( driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text)
        if(driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==cloneName):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[6]/button[1]"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[6]/button[1]"%(i)).click()
            sleep(5)      
            driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            sleep(2)
            #TBD: To check the status
            if(driver.find_element_by_xpath("//*[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr/td[6]/button[1]/span").text == ' Flattening'):
                logging.getLogger(caseName).info( "flatten %s successfully"%(cloneName))
            return
    return  
    ''' 

def deleteBlockDeviceClone(caseName, driver, cloneName): 
    driver.refresh()
    logging.getLogger(caseName).info( "delete clone ") 
    sleep(2)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/clone']").click()
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info( driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text)
        if(driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==cloneName):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[6]/button[2]/span"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_IMAGES_LIST_TABLE']/tbody/tr[%s]/td[6]/button[2]/span"%(i)).click()
            sleep(5)      
            driver.find_element_by_xpath("//a[@id='OK_BTN']").click()
            sleep(2)
            return
    return 

def setSnap(caseName,driver, imgName, snapNum):
    driver.refresh()
    logging.getLogger(caseName).info( "set snap for block device " ) 
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()  
    driver.find_element_by_id("iscsi-set-btn").click()  
    driver.find_element_by_xpath("//span[contains(@class, 'multiSelect')]").click()
    try:
        #driver.find_element_by_link_text(" "+imgName).click()
        imgElements = driver.find_elements_by_xpath("//div[contains(@class, 'acol')]//label//span")
        for elementItem in imgElements:
            if(elementItem.text.replace(" ", "") == imgName):
                elementItem.click()
    except:
        logging.getLogger(caseName).info( "No image found")
        sleep(30)
        #driver.close()
        return
    driver.find_element_by_xpath("//input[@type='number']").send_keys(snapNum) 
    driver.find_element_by_id("SUBMIT_BTN").click() 
    driver.refresh()
 
def createScheduleSnap(caseName, driver, imgName, snapScheduleName,interval):  
    driver.refresh()
    logging.getLogger(caseName).info( "create schedule snap")
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click() 
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshottask']").click()
    sleep(5)
    try:
        driver.find_element_by_id("iscsi-create-btn").click() 
    except:
        driver.find_element_by_id("iscsi-create-btn").click() 
    sleep(10)
    driver.find_element_by_xpath("//span[contains(@class, 'multiSelect')]").click()
    try:
        #driver.find_element_by_link_text(" "+imgName).click()
        imgElements = driver.find_elements_by_xpath("//div[contains(@class, 'acol')]//label//span")
        for elementItem in imgElements:
            if(elementItem.text.replace(" ", "") == imgName):
                elementItem.click()
    except:
        logging.getLogger(caseName).info( "No image found")
        sleep(30)
        #driver.close()
        return
    driver.find_element_by_id("CREATE_SNAPSHOT_FORM_NAME").send_keys(snapScheduleName)
    sleep(5)

    driver.find_element_by_xpath("//input[@type='number']").send_keys(interval)
    #driver.find_element_by_xpath("//input[@id='delete-old-snap']").click()
    try:
        driver.find_element_by_xpath("//span[contains(@class, 'ist-error-icon')]")
        logging.getLogger(caseName).info( "The name for snap is illegal ")
        #driver.close()
        return
    except:
        logging.getLogger(caseName).info( "element for snap name is right, now start to create snap")
    sleep(2)
    driver.find_element_by_id("SUBMIT_BTN").click() 
    driver.refresh()
 

def deleteScheduleSnap(caseName, driver, snapScheduleName):  
    driver.refresh()
    logging.getLogger(caseName).info( "delete schedule snap")
    sleep(1)
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click() 
    sleep(2)
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshottask']").click()
    sleep(2)
    #driver. find_element_by_xpath ("//span[contains(@class,'fa-trash')]").click()
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        logging.getLogger(caseName).info( driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text)
        if(driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ','') ==snapScheduleName):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[9]/button/span"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[9]/button/span"%(i)).click()
            sleep(5)      
            driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            sleep(2)
            break
            
    driver.refresh()
    driver.find_element_by_id(element.GOTO_STORAGEPOOLS).click()
    driver.find_element_by_xpath("//a[@href='/tbd/blockdeviceimages/snapshots']").click()
    rowCount = len (driver.find_elements_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr"))
    logging.getLogger(caseName).info( rowCount)
    for i in range(1, rowCount+1):
        if(re.findall(snapScheduleName, driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[2]"%(i)).text.replace(' ',''))):
            try:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[3]/span"%(i)).click()
            except:
                driver.find_element_by_xpath("//table[@id='CEPH_SNAPSHOTS_LIST_TABLE']/tbody/tr[%s]/td[8]/button[3]/span"%(i)).click()
            sleep(2)   
            ele = driver.find_element_by_xpath("//div[contains(@class,'modal-dialog-content')]")
            logging.getLogger(caseName).info(ele.text)
            #len(re.findall(r'eph-osd stop\/waiting',result))==1
            if(len(re.findall(r'There are ',ele.text))==1):
                logging.getLogger(caseName).info("clone found on snap")
                driver.refresh()
                return         
            driver.find_element_by_xpath("//*[@id='OK_BTN']").click()
            sleep(2)
            return
    #//*[@id="CEPH_IMAGES_LIST_TABLE"]/tbody/comment()[1]
    #//*[@id="CEPH_IMAGES_LIST_TABLE"]/tbody/tr[2]/td[7]/button[2]/span
    #//*[@id="CEPH_IMAGES_LIST_TABLE"]/tbody/tr[3]/td[7]/button[2]/span
       
