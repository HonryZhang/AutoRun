import logging
import sys
class LogRecord(object):
    def __init__(self, loggerName, logPath):
        self.mylogger = logging.getLogger(loggerName)
        self.mylogger.setLevel(logging.INFO)
        #wrtie the output to a file 
        self.fn = logging.FileHandler(logPath,'a')
        #set the format for the log
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s')        
        self.fn.setFormatter(self.formatter)
        self.mylogger.addHandler(self.fn)
        #write the output to console
        self.ch = logging.StreamHandler()  
        self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(self.formatter)
        self.mylogger.addHandler(self.ch)
        
        #self.mylogger.removeHandler(self.fn)
        #self.mylogger.removeHandler(self.ch)
    
    