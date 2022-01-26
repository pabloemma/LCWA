'''
Created on Apr 16, 2020

@author: klein

class to plot the speedtest results
is called by test_speed3
version which takes two different runs
'''

import matplotlib.pyplot as plt
import matplotlib.dates as md

import datetime
import numpy as np
import csv
import time
import sys
import os.path
import dropbox
import pandas as pd



class MyPlot(object):
    '''
    classdocs
    '''


    def __init__(self, path , filename , token , PlotFlag, runmode = 'Iperf'):
        '''
        Constructor
        file: is the speedtest filename
        token: is the dropbox file
        runmode is default iperf, however if it is both it will
        plot both resulst on same plot
        '''
        
        
        
        # First check for python version, this is important for the matlob read part
        self.MyPythonVersion()
        
        #now check if file is available, if not we exit
        
        file = path+'/'+filename
        
        if(self.IsFile(file)):
            self.InputFile = file
            self.output = self.InputFile.replace('csv','pdf')

        if(self.IsFile(token)):
            self.TokenFile = token
        
        self.dropbox_name = filename.replace('csv','pdf')
         
        self.path = path
        self.PlotFlag = PlotFlag    #Controls if there is a plot
         
        

    
    def MyPythonVersion(self):
        """ checks which version of python we are running
        """

        if (sys.version_info[0] == 3):
            print(' we have python 3')
            vers = True
        else:
            print('python2 not supported anymore')
            vers = False
            sys.exit(0)
        return vers

    
    
    
    def ReadFile(self):
        """ reads the csv file from the speedfile directory"""
        
        
        

    # read csv file into panda data dataframe
        temp_data = pd.read_csv(self.InputFile)
     # now we drop some of the columns, pay attention to white space
        drop_list =['server id','jitter','package','latency measured']
        
        lcwa_data = temp_data.drop(columns = drop_list)
        # convert date and time back to datetime
        lcwa_data["Time"] = pd.to_datetime(lcwa_data['time']) 

    # Create an iper and a speedtest frame

        iperf_opt = [' iperf3']
        self.lcwa_iperf = lcwa_data[lcwa_data['server name'].isin(iperf_opt)]  #all the iperf values
        self.lcwa_speed = lcwa_data[~lcwa_data['server name'].isin(iperf_opt)]  #all the not iperf values        
        


    def PlotData(self):
        """plots the data structure using pandas and matplotlib"""


        fig = plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax.text(.05,.95,'iperf and ookla on'+' '+self.DigIP(),weight='bold',transform=ax.transAxes,fontsize=11)

        ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')

        plt.title('Speedtest LCWA '+self.InputFile)



    
        plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["download"],'bs',label='\n iperf blue DOWN ')
        plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["upload"],'g^',label='\n iperf green UP ')
        plt.plot(self.lcwa_speed["Time"],self.lcwa_speed["download"],'ks',label='\n speedtest black DOWN ')
        plt.plot(self.lcwa_speed["Time"],self.lcwa_speed["upload"],'r^',label='\n speedtest red UP ')
        plt.ylim(0,40.)
        plt.grid(True)

        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True,fontsize = 6)
 
        print (self.output)
        fig.savefig(self.output, bbox_inches='tight')

    
        plt.show()

        
        






    

    

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

    def ConnectDropbox(self):
        """
        here we establish connection to the dropbox account
        """
        #f=open(self.keyfile,"r")
        #self.key =f.readline() #key for encryption
        #self.key = pad(self.key,16)
        #f.close()

        f=open(self.TokenFile,"r")
        self.data =f.readline() #key for encryption
        

         
         
         
         #connect to dropbox 
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))

        self.myaccount = self.dbx.users_get_current_account()
        print('***************************dropbox*******************\n\n\n')
        print( self.myaccount.name.surname , self.myaccount.name.given_name)
        print (self.myaccount.email)
        print('\n\n ***************************dropbox*******************\n')

    def DigIP(self):
        """ gets the ipaddress of the location"""
        
        stream = os.popen('dig +short myip.opendns.com @resolver1.opendns.com')
        return stream.read().strip('\n')
   
    
    
    def PushFileDropbox(self,dropdir):  
        f =open(self.output,"rb")

        self.dbx.files_upload(f.read(),dropdir+self.dropbox_name,mode=dropbox.files.WriteMode('overwrite', None))

       
if __name__ == '__main__':
    #path = '/home/pi/speedfiles'
    path = '/Users/klein/speedfiles'
    #file = 'misk_2022-01-24speedfile.csv'
    file = 'LC04_2022-01-26speedfile.csv'
    token ='/home/klein/git/speedtest/src/LCWA_d.txt'
    token ='/Users/klein/visual studio/LCWA/src/LCWA_d.txt'
    legend = {'IP':'63.233.221.150','Date':'more tests','Dropbox':'test', 'version':'5.01.01'}
    PlotFlag = True # flag to plot or not on screen
    MP = MyPlot(path,file,token,PlotFlag)
    MP.ReadFile()    #MP.ReadTestData(legend)
    MP.PlotData()
    MP.ConnectDropbox()
    MP.PushFileDropbox('/LCWA/ROTW/')
