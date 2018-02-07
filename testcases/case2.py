import os
from time import ctime,sleep
import logging
import inspect

def main(args):
    print os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    mylogger = logging.getLogger(os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0])

    for i in range(2):
        print "I was at the %s! %s" %(args,ctime())
        sleep(5)
    mylogger.info("second test case")
    print "second test case"
    print "second test case is running"
    print "second test case is end"
    return 1