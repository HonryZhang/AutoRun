import logging
import sys
import re
import os

class pool(object):
    def __init__(self, poolName, pgNumber):
        self.name = poolName
        self.pgNumber = pgNumber