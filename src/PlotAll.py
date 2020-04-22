'''
Created on Apr 21, 2020

@author: klein

Gets all the csv files from the different directories and plots them
'''



import dropbox
import datetime
import numpy as np
from pathlib import Path # this is python 3





class PlotAll(object):
    '''
    classdocs
    '''


    def __init__(self, token_file , dir_list):
        '''
        Constructor
        '''
        #File for dropbox key
        self.TokenFile =  token_file
        
        # List of directories to check
        self.DirList = dir_list
        
        
        
 
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


    def GetFiles(self):
        """
        This loops over the list of dropbox directories and gets the files for the current day if available
        """
        
        #First make the part of the file which is depending on the date
        MyFileName = self.GetCurrentFileName()
        
        #Here starts the loop
        for k in range(len(self.DirList)):
            temp = '/LCWA/'+self.DirList[k]+'/'+self.DirList[k]+MyFileName # file on dropbox
            temp_local = self.SetTempDirectory()+'/'+self.DirList[k]+MyFileName
            #print(temp)
            if self.DropFileExists(temp):
                print ("getting file " ,temp, '   and storing it at : ',temp_local)
                
                filename = self.dbx.files_download_to_file(temp_local,temp)

                


    def DropFileExists(self,path):
        try:
            self.dbx.files_get_metadata(path)
            return True
        except:
            return False        
        
        
    def GetCurrentFileName(self):
        """
        this creates the part of the current filename which depends on the date
        """
        self.current_day = datetime.date.today()
        a = datetime.datetime.today().strftime('%Y-%m-%d')
        return a+'speedfile.csv'  

    def ReadFile(self, InputFile):
        """ reads the csv file from the speedfile directory"""
        
        
        

        self.temp_file = open(self.SetTempDirectory()+'/temp.txt','w')
        counter = 0
        for line in open(InputFile, 'r'):
            a = line.split(',')
            if(len(a)< 9):
                print ('problem',a)
                print ('ignore data point at line ',counter+1)
            else:
                self.temp_file.write(line)

            counter = counter+1
            

        self.temp_file.close()
        
    def ReadTestData(self,legend):
        """
        Reads the results with Matplotlib
        """
        
        self.ReadFile()
        
        self.legend = legend #legend is a dictionary'
        
        if(self.MyPythonVersion):
           
            x1,y1,y2 = np.loadtxt(self.temp_name, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: self.MyTime},skiprows = 1)
            
        else:
          
                  
            x1,y1,y2 = np.loadtxt(self.temp_name, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.PlotTestData(x1, y1, y2)

    
    def SetTempDirectory(self):
        """ 
        this sets the directory for storing temporary files
        if the directory dos not exist it gets created. It is the scratch directory
        below the home directory
        """
        home = str(Path.home()) # get the home directory
        MyTempDir = home+'/scratch'
        # Now check if it exists, if no create it
        if(Path(MyTempDir)).exists():
            return MyTempDir
        else:
            Path(MyTempDir).mkdir()
            print(" Creating  ",MyTempDir)
            return MyTempDir
            
        
        
 
 
if __name__ == '__main__':
    #create the list
    temp = 'LC'
    dirlist = []
    for k in range(1,11):
        if (k<10):
            temp1 = temp+'0'+str(k)+'_'
        else:
            temp1 = temp+str(k)+'_'
            
        dirlist.append(temp1)
    token_file = '/Users/klein/git/LCWA/src/LCWA_d.txt'
    tempdir = 'scratch'
    PA=PlotAll(token_file,dirlist)
    PA.ConnectDropbox()
    PA.GetFiles()