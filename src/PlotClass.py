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
#import logging
from loguru import logger


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
        
        #old logger logger = logging.getLogger(__name__)
        #logger.info('Startlogging in set time:')

        
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
            logger.info(' we have python 3')
            vers = True
        else:
            logger.error('python2 not supported anymore')
            vers = False
            sys.exit(0)
        return vers

    
    
    
    #def ReadFile(self):
    def ReadTestData(self):
        """ reads the csv file from the speedfile directory"""
        
        
        

    # read csv file into panda data dataframe
        temp_data = pd.read_csv(self.InputFile)
      # now we drop some of the columns, pay attention to white space
        #drop_list =['server id','jitter','package','latency measured']
        drop_list =['server id']
        #print(temp_data)
        try:
            lcwa_data = temp_data.drop(columns = drop_list)
        except:
            logger.error('error in pandas')
            return
        # convert date and time back to datetime
        lcwa_data["Time"] = pd.to_datetime(lcwa_data['time'], format='%H:%M:%S') 

    # Create an iper and a speedtest frame

        iperf_opt = [' iperf3']
        self.lcwa_iperf = lcwa_data[lcwa_data['server name'].isin(iperf_opt)]  #all the iperf values
        self.lcwa_speed = lcwa_data[~lcwa_data['server name'].isin(iperf_opt)]  #all the not iperf values        

        self.PlotData()    


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
        plt.plot(self.lcwa_speed["Time"],self.lcwa_speed["jitter"],'y^',label='\n jitter yellow  ')
        plt.plot(self.lcwa_speed["Time"],self.lcwa_speed["latency measured"],'m^',label='\n latency measured magenta  ')
        plt.plot(self.lcwa_speed["Time"],self.lcwa_speed["package"],'c^',label='\n package loss cyan  ')
        


        # remove limit
        plt.ylim(bottom = 0.)
        # simple determination of scaling
        if(self.lcwa_speed['download'].max() > 80.):
            ymax = 120.
        elif(self.lcwa_speed['download'].max() > 45.):
            ymax = 60.
        elif(self.lcwa_speed['download'].max() > 15.):
            ymax = 30.
        
        
        #plt.ylim(top = 1.10*self.lcwa_speed['download'].max())
        plt.ylim(top = ymax)
        plt.grid(True)

        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.legend(facecolor='ivory',loc="center left",shadow=True, fancybox=True,fontsize = 6)
        temp_txt = str(self.output)
        logger.info(temp_txt)
        fig.savefig(self.output, bbox_inches='tight')

    
        plt.show()

        
        

    def Analyze(self, filename = None):
        """analyze the data we collected"""

        # determine a few statistical values
        #first the min and max for either one
        # ipewf
        if not self.lcwa_iperf.empty:
            iperf_min_dw    = self.lcwa_iperf['download'].min() # min
            iperf_max_dw    = self.lcwa_iperf['download'].max() # max
            iperf_corrected = self.CorrectedStd(self.lcwa_iperf['download']) # recalculate std with min removed
            

            iperf_min_up    = self.lcwa_iperf['upload'].min() # min
            iperf_max_up    = self.lcwa_iperf['upload'].max() #max

            iperf_mean_up   = self.lcwa_iperf['upload'].mean() # mean of distribution
            iperf_std_up    = self.lcwa_iperf['upload'].std() # standard deviation of distribution

            iperf_mean_dw   = self.lcwa_iperf['download'].mean() # mean of distribution
            iperf_std_dw    = self.lcwa_iperf['download'].std() # standard deviation of distribution

        if not self.lcwa_speed.empty:
            speed_min_dw    = self.lcwa_speed['download'].min() # min
            speed_max_dw    = self.lcwa_speed['download'].max() # max
            speed_corrected = self.CorrectedStd(self.lcwa_speed['download'])

            speed_min_up    = self.lcwa_speed['upload'].min() # min
            speed_max_up    = self.lcwa_speed['upload'].max() #max

            speed_mean_up   = self.lcwa_speed['upload'].mean() # mean of distribution
            speed_std_up    = self.lcwa_speed['upload'].std() # standard deviation of distribution

            speed_mean_dw   = self.lcwa_speed['download'].mean() # mean of distribution
            speed_std_dw    = self.lcwa_speed['download'].std() # standard deviation of distribution
            bfb = '\033[1m'
            bfe = '\033[0m'

        # here we print out the statistics
            if(filename == None):
 

                print('\n\n ********************************total statistics********************** \n')
                if not self.lcwa_iperf.empty:
    
                    print(bfb,'Iperf:',bfe)
                    print('Min download                 = ',iperf_min_dw,'    Min corrected             =',iperf_corrected[1])
                    print('Max download                 = ',iperf_max_dw)
                    print('Mean download                = ',iperf_mean_dw)
                    print('Std download                 = ',iperf_std_dw ,'   Std corrected             =',iperf_corrected[0],'\n')
   
                    print('Min upload                   = ',iperf_min_up)
                    print('Max upload                   = ',iperf_max_up)
                    print('Mean upload                  = ',iperf_mean_up)
                    print('Std upload                   = ',iperf_std_up , '\n\n')
                if not self.lcwa_speed.empty:
    
                    print(bfb,'Ookla Speedtest:',bfe)
                    print('Min download                 = ',speed_min_dw,'    Min corrected             =',speed_corrected[1])
                    print('Max download                 = ',speed_max_dw)
                    print('Mean download                = ',speed_mean_dw)
                    print('Std download                 = ',speed_std_dw ,'   Std corrected             =',speed_corrected[0],'\n')
   
                    print('Min upload                   = ',speed_min_up)
                    print('Max upload                   = ',speed_max_up)
                    print('Mean upload                  = ',speed_mean_up)
                    print('Std upload                   = ',speed_std_up , '\n\n')
                
                
                
     
                print('\n\n ********************************end statistics********************** \n')
 
            else:
                if not self.lcwa_iperf.empty:


                    
                    str_iperf_min_d = 'Min download                 = '+str(iperf_min_dw)+'    Min corrected             ='+str(iperf_corrected[1]) +'\n'
 				
                    str_iperf_max_d = 'Max download                 = '+str(iperf_max_dw)+'\n'
                    str_iperf_mean_d = 'Mean download                 = '+str(iperf_mean_dw)+'\n'

 			    
                    str_iperf_std_d = 'Std download                 = '+str(iperf_std_dw)+'    Std corrected             ='+str(iperf_corrected[0]) +'\n'
  
			     
                    str_iperf_min_u = 'Min upload                 = '+str(iperf_min_up) +'\n'
 			    
                    str_iperf_max_u = 'Max upload                 = '+str(iperf_max_up)+'\n'
 				
                    str_iperf_mean_u = 'Mean upload                 = '+str(iperf_mean_up)+'\n'
 				
                    str_iperf_std_u = 'Std upload                 = '+str(iperf_std_up)+'\n'
 			
                if not self.lcwa_speed.empty:
                    str_speed_min_d = 'Min download                 = '+str(speed_min_dw)+'    Min corrected             ='+str(speed_corrected[1])+'\n'
 			
                    str_speed_max_d = 'Max download                 = '+str(speed_max_dw)+'\n'
 				
                    str_speed_mean_d = 'Mean download                 = '+str(speed_mean_dw)+'\n'
 				
                    str_speed_std_d = 'Std download                 = '+str(speed_std_dw)+'    Std corrected             ='+str(speed_corrected[0])+'\n'
  
                    str_speed_min_u = 'Min upload                 = '+str(speed_min_up)+'\n'
 				
                    str_speed_max_u = 'Max upload                 = '+str(speed_max_up)+'\n'
 				
                    str_speed_mean_u = 'Mean upload                 = '+str(speed_mean_up)+'\n'
 				
                    str_speed_std_u = 'Std upload                 = '+str(speed_std_up)+'\n'
 				
				
                #check if file exists
                f = open(filename,"a")
                f.write('\n\n ********************************total statistics********************** \n')
                line = 'Iperf \n'
                f.write(line)
                #f.write(str(self.lcwa_iperf['download'].describe()))
                #f.write(str(self.lcwa_iperf['upload'].describe()))
                if not self.lcwa_iperf.empty:
                
                    f.write(str_iperf_min_d)
                    f.write(str_iperf_max_d)
                    f.write(str_iperf_mean_d)
                    f.write(str_iperf_std_d)
                
                    f.write(str_iperf_min_u)
                    f.write(str_iperf_max_u)
                    f.write(str_iperf_mean_u)
                    f.write(str_iperf_std_u)
                
                if not self.lcwa_speed.empty:
               
                    f.write('\n\n')
                    line ='Ookla Speedtest \n'
 
                    f.write(line)
                #f.write(str(self.lcwa_speed['download'].describe()))
                #f.write(str(self.lcwa_speed['upload'].describe()))
                
                    f.write(str_speed_min_d)
                    f.write(str_speed_max_d)
                    f.write(str_speed_mean_d)
                    f.write(str_speed_std_d)
                
                    f.write(str_speed_min_u)
                    f.write(str_speed_max_u)
                    f.write(str_speed_mean_u)
                    f.write(str_speed_std_u)
                
                f.write('\n\n ********************************end statistics********************** \n')
   
                
                f.close()


    def CorrectedStd(self,data):
        """calculates the std of the distribution with removin smallest point"""
        # first find the index of min
        temp = data.idxmin()

        # remove the min number and create new structure
        new_data = data.drop(temp)
        #print(new_data.std(),new_data.min())
        temp_list = [new_data.std(),new_data.min()]
        return temp_list
    

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
            temp_txt = 'no file:   ' + str(filename)
            logger.error(temp_txt)
            sys.exit(0)

    def ConnectDropboxOld(self):
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

    def ConnectDropBox(self):
        """
        here we establish connection to the dropbox account
        """
        logger.info("at connect dropbox")
        #self.TokenFile=self.cryptofile.strip('\n')
        #f=open(self.TokenFile,"r")

        # now we branch out depending on which keyfile we are using:
        if  'LCWA_d.txt' in self.TokenFile:
            logger.info("old system")
            f=open(self.TokenFile,"r")
            self.data =f.readline() #key for encryption
        

         
         
         
         #connect to dropbox 
            self.dbx=dropbox.Dropbox(self.data.strip('\n'))
            temp_txt ="self.dbx"+str(self.dbx)
            print(temp_txt)

 
        elif 'LCWA_a.txt'  in self.TokenFile:
            logger.info('new system')
            f=open(self.TokenFile,"r")
  
            temp =f.readlines() #key for encryption
            temp_buf = []
  
            for k in range(len(temp)):
                temp1 = temp[k].strip('\n')
                start   = temp1.find('\'') # find beginning quote
                end     = temp1.rfind('\'') # find trailing  quote
                temp_buf.append(temp1[start+1:end])
        
        


        
    
             #connect to dropbox 
            #self.dbx=dropbox.Dropbox(self.data.strip('\n'))
            APP_KEY = temp_buf[0]
            APP_SECRET = temp_buf[1]
            REFRESH_TOKEN = temp_buf[2]

            



            self.dbx = dropbox.Dropbox(
                app_key = APP_KEY,
                app_secret = APP_SECRET,
                oauth2_refresh_token = REFRESH_TOKEN
                )
            temp_txt = 'self.dbx'+str(self.dbx)
            logger.info(temp_txt)

        
        else:
            logger.error("wrong keyfile")


        

        self.myaccount = self.dbx.users_get_current_account()
     

        logger.info('***************************dropbox*******************\n\n\n')
        my_credentials = self.myaccount.name.surname +' '+ self.myaccount.name.given_name
        logger.info(my_credentials)
        my_email = self.myaccount.email
        logger.info(my_email+'\n\n')
        logger.info('***************************dropbox*******************\n')



        return self.dbx





    def DigIP(self):
        """ gets the ipaddress of the location"""
        
        stream = os.popen('dig +short myip.opendns.com @resolver1.opendns.com')
        return stream.read().strip('\n')
   
    def ReturnNames(self,dropdir):
        """ Kludge since pushfile from test_speed does not work
        I suspect a problem with the pointer"""
        temp = [dropdir,self.output,self.dropbox_name]
        return temp
    
    
    def PushFileDropbox(self,dropdir): 
         
        f =open(self.output,"rb")
        #print('plotclass1  ',dropdir,self.output,self.dropbox_name)

        a = self.dbx.files_upload(f.read(),dropdir+self.dropbox_name,mode=dropbox.files.WriteMode('overwrite', None))
        #print('this is a',a)
       
if __name__ == '__main__':
    #path = '/home/pi/speedfiles'
    path = '/Users/klein/speedfiles'
    #path='/Users/klein/scratch/'
    file = 'LC20_2024-03-28speedfile.csv'
    #file = 'LC04_2022-02-14speedfile.csv'
    token ='/Users/klein/git/LCWA/src/LCWA_a.txt'
    #token ='/Users/klein/visual studio/LCWA/src/LCWA_d.txt'
    legend = {'IP':'63.233.221.150','Date':'more tests','Dropbox':'test', 'version':'5.01.01'}
    PlotFlag = True # flag to plot or not on screen
    MP = MyPlot(path,file,token,PlotFlag)
    MP.ConnectDropBox()
    MP.ReadTestData()    #MP.ReadTestData(legend)
    #MP.Analyze('/home/klein/scratch/text.txt')
    MP.Analyze()
    MP.PushFileDropbox('/LCWA/LC04/')
