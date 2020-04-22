'''
Created on Apr 21, 2020

@author: klein

Gets all the csv files from the different directories and plots them
'''



import dropbox
import datetime
import numpy as np
from pathlib import Path # this is python 3
import matplotlib.pyplot as plt
import matplotlib.dates as md





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
        
        #next block determines how many graphs we will do
        graph_count = 0

        for k in range(len(self.DirList)):
            temp = '/LCWA/'+self.DirList[k]+'/'+self.DirList[k]+MyFileName # file on dropbox
            if self.DropFileExists(temp):
                graph_count = graph_count+1

        print ('we have ',graph_count,'  plots')
        
        
        #Here starts the loop
        for k in range(len(self.DirList)):
            temp = '/LCWA/'+self.DirList[k]+'/'+self.DirList[k]+MyFileName # file on dropbox
            temp_local = self.SetTempDirectory()+'/'+self.DirList[k]+MyFileName
            #print(temp)
            if self.DropFileExists(temp):
                print ("getting file " ,temp, '   and storing it at : ',temp_local)
                
                filename = self.dbx.files_download_to_file(temp_local,temp)
                
                # Read the local file
                self.ReadFile(temp_local)

                self.ReadTestData()
                


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
        
        
        
        self.temp_name = self.SetTempDirectory()+'/temp.txt'
        self.temp_file = open(self.temp_name,'w')
        counter = 0
        for line in open(InputFile, 'r'):
            a = line.split(',')
            if(counter==0):
                self.MyIP =a[0].strip('day')
            if(len(a)< 9):
                print ('problem',a)
                print ('ignore data point at line ',counter+1)
            else:
                self.temp_file.write(line)

            counter = counter+1
            

        self.temp_file.close()
        
    def ReadTestData(self):
        """
        Reads the results with Matplotlib
        """
        
        
        #self.legend = legend #legend is a dictionary'
        
           
        x1,y1,y2 = np.loadtxt(self.temp_name, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: self.MyTime},skiprows = 1)
            
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2

    
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
            
    def MyTime(self,b):
        """ conversion routine for time to be used in Matplotlib"""

        
        s=b.decode('ascii')
        
        a =md.date2num(datetime.datetime.strptime(s,'%H:%M:%S'))    
        
        return a
    
    
    def PlotSetup(self,graph_count):
        """
        Creates the plotting environment
        """
        
        
    
    
        
    def PlotTestData(self,x1,y1,y2):
        """
        Plots the tests
        """
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        
        #Add Ip address
        
        
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)

        #add legend
        print(self.legend)
        ax.text(.05,.95,'MyIP = '+self.DigIP(),weight='bold',transform=ax.transAxes,fontsize=11)

        plt.plot_date(x1,y1,'bs',label='\n blue DOWN ')
        plt.plot_date(x1,y2,'g^',label=' green UP')
        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')

        plt.title('Speedtest LCWA '+self.InputFile)
    
        plt.legend(facecolor='ivory',loc="upper right",shadow=True, fancybox=True)
        plt.ylim(0.,24.) # set yaxis limit
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        print('input file',self.InputFile)

        print (self.output)
        fig.savefig(self.output, bbox_inches='tight')
        if(self.PlotFlag):
            plt.show()  #Uncomment for seeing the plot
        
 
 
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