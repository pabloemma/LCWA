'''
Created on May 8, 2023

@author: klein

test connection to dropbox
'''



import dropbox
import datetime
import time
from pathlib import Path 
from os.path import expanduser

class TestDropBox(object):

    def __init__(self,local_dir = None , dropbox_dir = None , dropbox_file = None, tokenfile = None, loop_time = None):
        self.LoopTime        = loop_time
        self.TokenFile      = tokenfile
        self.DropBoxFile    = dropbox_file
        self.DropBoxDir     = dropbox_dir
        self.LocalDir       = local_dir

    def ConnectDropbox(self):
        """
        here we establish connection to the dropbox account
        """
        f=open(self.TokenFile,"r")
        self.data =f.readline() #key for encryption
        
    
             #connect to dropbox 
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))

        self.myaccount = self.dbx.users_get_current_account()
        print('***************************dropbox*******************\n\n\n')
        print( self.myaccount.name.surname , self.myaccount.name.given_name)
        print (self.myaccount.email)
        print('\n\n ***************************dropbox*******************\n')

        return


    def DropFileExists(self,path):
        try:
            self.dbx.files_get_metadata(path)
            return True
        except:
            return False  
              

        

    def GetDropBoxfile(self , temp):

        if self.DropFileExists(temp):
            print ("getting file " ,temp, '   and storing it at : ',self.LocalDir+self.DropBoxFile)
                
            self.dbx.files_download_to_file(self.LocalDir+self.DropBoxFile,temp)
            return True
        
        else:
            return False
     
         
         

    def MainLoop(self):
        ''' this a timed loop, which every looptime gets the file at dropbox
        looptime is seconds
        '''
        while(True):
            e = datetime.datetime.now()
            if self.GetDropBoxfile(self.DropBoxDir+self.DropBoxFile):
                print(" Succesful Transfer at : %s/%s/%s  %s:%s:%s" % (e.day, e.month, e.year,e.hour, e.minute, e.second))
            else:
                print(" Failed Transfer at : %s/%s/%s  %s:%s:%s" % (e.day, e.month, e.year,e.hour, e.minute, e.second))

            time.sleep(self.LoopTime)  

        return 

 

if __name__ == '__main__':
    import os.path
    loop_time       = 600 # every loop_time we will read a file and copy it locally, the time is in seconds
    homedir         = os.path.expanduser('~')
    tokenfile       = homedir+'/git/LCWA/src/LCWA_d.txt'
    dropbox_dir     = '/LCWA/ALL_LCWA/' # dir on dropbox
    dropbox_file    = 'LCWA_TOTAL_2023-05-07speedfile.pdf'
    local_dir       = homedir+'/scratch/'


    TDB = TestDropBox(local_dir = local_dir ,dropbox_dir = dropbox_dir , dropbox_file = dropbox_file,  tokenfile = tokenfile ,loop_time = loop_time)
    TDB.ConnectDropbox()
    TDB.MainLoop()