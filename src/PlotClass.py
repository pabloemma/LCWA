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

    
    
    
    #def ReadFile(self):
    def ReadTestData(self):
        """ reads the csv file from the speedfile directory"""
        
        
        

    # read csv file into panda data dataframe
        temp_data = pd.read_csv(self.InputFile)
      # now we drop some of the columns, pay attention to white space
        drop_list =['server id','jitter','package','latency measured']
        print(temp_data)
        
        lcwa_data = temp_data.drop(columns = drop_list)
        # convert date and time back to datetime
        lcwa_data["Time"] = pd.to_datetime(lcwa_data['time']) 

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

        # remove limit
        # plt.ylim(0,40.)
        plt.grid(True)

        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True,fontsize = 6)
 
        print (self.output)
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

            iperf_min_up    = self.lcwa_iperf['upload'].min() # min
            iperf_max_up    = self.lcwa_iperf['upload'].max() #max

            iperf_mean_up   = self.lcwa_iperf['upload'].mean() # mean of distribution
            iperf_std_up    = self.lcwa_iperf['upload'].std() # standard deviation of distribution

            iperf_mean_dw   = self.lcwa_iperf['download'].mean() # mean of distribution
            iperf_std_dw    = self.lcwa_iperf['download'].std() # standard deviation of distribution

        if not self.lcwa_speed.empty:
            speed_min_dw    = self.lcwa_speed['download'].min() # min
            speed_max_dw    = self.lcwa_speed['download'].max() # max

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
                print(bfb,'Iperf:',bfe)
                print('Min download                 = ',iperf_min_dw)
                print('Max download                 = ',iperf_max_dw)
                print('Mean download                = ',iperf_mean_dw)
                print('std download                 = ',iperf_std_dw , '\n')
   
                print('Min upload                   = ',iperf_min_up)
                print('Max upload                   = ',iperf_max_up)
                print('Mean upload                  = ',iperf_mean_up)
                print('std upload                   = ',iperf_std_up , '\n\n')
   
                print(bfb,'Ookla Speedtest:',bfe)
                print('Min download                 = ',speed_min_dw)
                print('Max download                 = ',speed_max_dw)
                print('Mean download                = ',speed_mean_dw)
                print('std download                 = ',speed_std_dw , '\n')
   
                print('Min upload                   = ',speed_min_up)
                print('Max upload                   = ',speed_max_up)
                print('Mean upload                  = ',speed_mean_up)
                print('std upload                   = ',speed_std_up , '\n\n')
                
                
                
     
                print('\n\n ********************************end statistics********************** \n')
 
            else:
			    
                str_iperf_min_d = 'Min download                 = '+str(iperf_min_dw)+'\n'
 				
                str_iperf_max_d = 'Max download                 = '+str(iperf_max_dw)+'\n'
                str_iperf_mean_d = 'Mean download                 = '+str(iperf_mean_dw)+'\n'

 			    
                str_iperf_std_d = 'Std download                 = '+str(iperf_std_dw)+'\n'
  
			     
                str_iperf_min_u = 'Min upload                 = '+str(iperf_min_up)+'\n'
 			    
                str_iperf_max_u = 'Max upload                 = '+str(iperf_max_up)+'\n'
 				
                str_iperf_mean_u = 'Mean upload                 = '+str(iperf_mean_up)+'\n'
 				
                str_iperf_std_u = 'Std upload                 = '+str(iperf_std_up)+'\n'
 			
				
                str_speed_min_d = 'Min download                 = '+str(speed_min_dw)+'\n'
 			
                str_speed_max_d = 'Max download                 = '+str(speed_max_dw)+'\n'
 				
                str_speed_mean_d = 'Mean download                 = '+str(speed_mean_dw)+'\n'
 				
                str_speed_std_d = 'Std download                 = '+str(speed_std_dw)+'\n'
  
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
                
                f.write(str_iperf_min_d)
                f.write(str_iperf_max_d)
                f.write(str_iperf_mean_d)
                f.write(str_iperf_std_d)
                
                f.write(str_iperf_min_u)
                f.write(str_iperf_max_u)
                f.write(str_iperf_mean_u)
                f.write(str_iperf_std_u)
                
                
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
        #print('plotclass1  ',dropdir,self.output,self.dropbox_name)

        self.dbx.files_upload(f.read(),dropdir+self.dropbox_name,mode=dropbox.files.WriteMode('overwrite', None))

       
if __name__ == '__main__':
    #path = '/home/pi/speedfiles'
    path = '/home/klein/speedfiles'
    #file = 'misk_2022-01-24speedfile.csv'
    file = 'LC23_2022-01-28speedfile.csv'
    token ='/home/klein/git/speedtest/src/LCWA_d.txt'
    token ='/Users/klein/visual studio/LCWA/src/LCWA_d.txt'
    legend = {'IP':'63.233.221.150','Date':'more tests','Dropbox':'test', 'version':'5.01.01'}
    PlotFlag = True # flag to plot or not on screen
    MP = MyPlot(path,file,token,PlotFlag)
    MP.ReadTestData()    #MP.ReadTestData(legend)
    MP.Analyze('/home/klein/scratch/text.txt')
    MP.Analyze()
