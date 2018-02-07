import os, inspect
import sys
import re

def add(arg1, arg2):
    return str(eval(re.sub('[^\d\+]','',arg1)) + eval(re.sub('[^\d\+]','',arg2))) + re.sub('[^a-zA-Z]','',arg1)

def sub(arg1, arg2):
    return str(eval(re.sub('[^\d\+]','',arg1)) - eval(re.sub('[^\d\+]','',arg2))) + re.sub('[^a-zA-Z]','',arg1)
    