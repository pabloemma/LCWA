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
import dropbox



class MyPlot(object):
    '''
    classdocs
    '''


    def __init__(self, path , filename , token):
        '''
        Constructor
        file: is the speedtest filename
        token: is the dropbox file
        '''
        
        
        
        # First check for python version, this is important for the matlob read part
        self.MyPythonVersion()
        
        #now check if file is available, if not we exit
        
        file = path+'/'+filename
        
        if(self.IsFile(file)):
            self.InputFile = file
        if(self.IsFile(token)):
            self.TokenFile = token
        
        self.dropbox_name = filename.replace('csv','pdf')
         
        self.path = path    
        
        

    
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

    
    
    
    def ReadFile(self):
        """ reads the csv file from the speedfile directory"""
        
        
        
        
        self.temp_file = open(self.path+'/temp.txt',"r+")
        counter = 0
        for line in open(self.InputFile, 'r'):
            print(line)
            a = line.split(',')
            if(len(a)< 9):
                print ('problem',a)
                print ('ignore data point at line ',counter+1)
            else:
                self.temp_file.write(line)

            counter = counter+1
            print('counter',counter)
            

        #self.temp_file.close()
        
    def ReadTestData(self):
        """
        Reads the results with Matplotlib
        """
        
        self.ReadFile()
        self.temp_file.seek(0)

        if(self.MyPythonVersion):
            x1,y1,y2 = np.loadtxt(self.temp_file, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: self.MyTime},skiprows =1)
        else:      
            x1,y1,y2 = np.loadtxt(self.temp_file, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.PlotTestData(x1, y1, y2)
        
    
    def PlotTestData(self,x1,y1,y2):
        """
        Plots the tests
        """
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)

        plt.plot_date(x1,y1,'bs',label='\n blue DOWN ')
        plt.plot_date(x1,y2,'g^',label=' green UP')
        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')

        plt.title('Speedtest LCWA using '+self.InputFile)
    
        plt.legend(facecolor='ivory',loc="lower right",shadow=True, fancybox=True)
        plt.ylim(0.,24.) # set yaxis limit
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        self.output = self.InputFile.replace('csv','pdf')

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

    
    
    
    def PushFileDropbox(self):  
        f =open(self.output,"rb")

        self.dbx.files_upload(f.read(),'/LCWA/'+self.dropbox_name,mode=dropbox.files.WriteMode('overwrite', None))

       
if __name__ == '__main__':
    path = '/Users/klein/speedfiles'
    file = 'Pand_2020-03-02speedfile.csv'
    token ='/Users/klein/git/speedtest/LCWA/src/LCWA_d.txt'
    MP = MyPlot(path,file,token)
    MP.ReadTestData()
    MP.ConnectDropbox()
    MP.PushFileDropbox()
