import sys,imp,os,traceback
import os
import sys
import logs
import thread
import threading
import Queue
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
#from wx.tools.XRCed.images import TreeRoot
import time
import getopt

help  = False
testset = ""
testEnv = ""
usage='''
usage: python AutoRun.py -e testEnv.xml -s testSet.xml
-e: testEnvironment information xml file
-s: testCase set information xml file
-h: help
'''
def getOpts():
    global testset
    global testEnv
    global help
    options, remainder = getopt.getopt(sys.argv[1:], 'e:s:h', ['environment=', 
                                                     'testset=',
                                                     'help'
                                                     ])
    for opt, arg in options:
        if opt in ('-e', '--environment'):
            testEnv = arg
        elif opt in ('-s','--testset'):
            testset = arg
        elif opt in ('-h','--help'):
            help = True
    if(len(testEnv) == 0 or len(testset) == 0) and (not help):
        print "The parameter you entered is invalid, please use -h or --help for help"
        exit()
    if(help):
        print usage 
        exit()
    return
        
def mklogDir():
    currentLogDir = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))    
    currentLogDir = sys.path[0]+'/logs/'+currentLogDir
    if not os.path.exists(currentLogDir):
        os.mkdir(currentLogDir)
    else:
        os.removedirs(currentLogDir)
        os.mkdir(currentLogDir)
    return currentLogDir
    
def load(module_name,module_path):
    print imp.find_module(module_name,[module_path])
    fp, pathname, description=imp.find_module(module_name,[module_path])
    try:
        return imp.load_module(module_name,fp,pathname,description)
    finally:
        if fp:
            fp.close()
            
def do(module_name,module_path,module_args):
    sys.path.append(module_path) 
    default_cwd=os.getcwd()    
    try:
        
        do=load(module_name,module_path)
        exit_code=do.main(module_args) #the args for main is string
        if exit_code==-1:
            print('execute error')
            exit(0)
    except:
        vtype,value,trace=sys.exc_info()
        error_string=traceback.format_exception(vtype,value,trace)
        print(error_string)
        return 0
    sys.path.pop()
    os.chdir(default_cwd)
    #thread.exit_thread()  

def doMultiple(module_name,module_path,module_args):
    do(module_name,module_path,module_args)
    thread.exit_thread()
    
def getCasesLocation(testset):
    testEnvTree = ET.parse(testset)
    treeRoot = testEnvTree.getroot()
    caseLocationDict = {}
    for test in treeRoot.findall('testcases/test'):
        caseName = test.attrib['id'] +'@'+ test.attrib['name']
        #caseId = test.attrib['id']
        caseLocation = test.find('location').text
        #caseLocationList.append(caseLocation)
        caseLocationDict[caseName] = caseLocation
    return caseLocationDict

def getGeneralParams(testset):
    testEnvTree = ET.parse(testset)
    treeRoot = testEnvTree.getroot()
    #generalParamList = []  
    generalParamDict = {}  
    for param in treeRoot.findall('general_case_parameters/param'):        
        generalParamName = param.attrib['name']
        generalParamValue = param.attrib['value']
        generalParamDict[generalParamName] = generalParamValue
    return generalParamDict

def callCases(caseLocationDict, generalParamDict, testEnv):
    #print caseLocationDict
    logDir = mklogDir()
    keys = caseLocationDict.keys()
    keys.sort()

    if(('parallel' in generalParamDict.keys()) and (generalParamDict['parallel'] == '1')):
        #start multiple threads
        print 'parallel'
        #queue = Queue.Queue()
        #Init the queue

        for caseName in keys:
            #queue.put(caseName)
            caseLocation = './'+caseLocationDict[caseName]  
            caseName = caseName.split('@')[1]
            logPath = logDir +'/' + caseName +'.log'
            logRecord=logs.LogRecord(caseName, logPath)
            t =threading.Thread(target=doMultiple, args=(caseName,os.path.dirname('./'+caseLocation),testEnv))
            t.setDaemon(True)
            t.start()

        if(('stopOnError' in generalParamDict.keys()) and (generalParamDict['stopOnError'] == '1')):  
            return
        else:  
            t.join()
        print "case running end"
    else:
        #one by one
        print caseLocationDict.keys()        
        for caseName in keys:
            caseLocation = './'+caseLocationDict[caseName]    
            print caseName 
            caseName = caseName.split('@')[1]     
            #print caseLocation
            logPath = logDir +'/' + caseName +'.log'
            #logRecord=logs.LogRecord(caseName, logPath)
            logs.LogRecord(caseName, logPath)
            returnCode = do(caseName,os.path.dirname(caseLocation),testEnv)
            #If stop on error is set           
            if(('stopOnError' in generalParamDict.keys()) and (generalParamDict['stopOnError'] == '1')):
                if (returnCode == 0):#case fail
                    break            
    return
        
if __name__ == "__main__":
    getOpts()
    print "test set file is %s"%testset
    print "test env file is %s"%testEnv
    caseLocationDict =  getCasesLocation(testset)    
    print caseLocationDict
    generalParamDict =  getGeneralParams(testset)
    callCases(caseLocationDict, generalParamDict, testEnv)
    