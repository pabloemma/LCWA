'''
Created on Apr 16, 2020

@author: klein

class to plot the speedtest results
is called by test_speed3
'''

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
import numpy as np
import csv
import time
import sys
import os.path
from builtins import True
#import dropbox



class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, file , token):
        '''
        Constructor
        file: is the speedtest filename
        token: is the dropbox file
        '''
        
        
        
        # First check for python version, this is important for the matlob read part
        self.MyPythonVersion()
        
        #now check if file is available, if not we exit
        if(self.IsFile(file)):
            self.InputFile = file
        if(self.IsFile(token)):
            self.TokenFile = token
         
            
        
        

    
    def MyPythonVersion(self):
        """ checks which version of python we are running
        """

        if (sys.version_info[0] == 3):
            print(' we have python 3')
            vers = True
        else:
            print(' you should switch to python 2')
            vers = False
        return vers

    
    
    def MyTime(self,b):
        """ conversion routine for time to be used in Matplotlib"""

        
        s=b.decode('ascii')
        
        a =md.date2num(datetime.datetime.strptime(s,'%H:%M:%S'))    
        
        return a
    
    

    def IsFile(self,filename):
        """checks if file exists"""
        
        try:
            os.path.isfile(filename)
            return True
        
        except:
            print('no file:   ' , filename)
            sys.exit(0)

       
       
if __name__ == '__main__':
    pass 