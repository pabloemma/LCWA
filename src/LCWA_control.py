'''
Created on Apr 24, 2020

@author: klein
'''

import PlotAll as PL
import dropbox
import datetime
import SendFileMail as SFM
import os
import datetime


class MyControl(object):
    '''
    this class runs plotall and does some housekeeping at dropbox
    '''


    def __init__(self, backupdir):
        '''
        Constructor
        '''
        
        
        #first get everything setup with dropbox by excuting DoPlotting
        
        self.backupdir = backupdir
        
        self.DoPlotting()
        
        self.CleanupDropbox()
        
        
        
    def CleanupDropbox(self):
        """
        Here we go into the dropbox directories and check for old files (older than a week)
        """
        
        
        #loop over directories and check if anyone has something older than one week
        temp = 'LC'
        dirlist = []
        for k in range(1,16):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
            
        for k in range(len(dirlist)):
            temp = '/LCWA/'+dirlist[k] # file on dropbox
            print('now checking ',temp)

        
            MyDir = self.PA.dbx.files_list_folder(temp) #do NOT use recursive, since that does not work for shared folders
        
            for item in MyDir.entries:
                if isinstance(item, dropbox.files.FileMetadata):
                    now = datetime.datetime.now() #determine how old a file is
                    diff = now - item.server_modified #take the difference
                    if(diff.days > 8 ):
                        print ('name = ' , item.name)
                        print ('path  = ', item.path_display )
                        print ('fileID = ' , item.id)
                        print ('date = ', item.server_modified)
                    # here we backup and delete the files
                        backupfile = self.backupdir+item.name
                        print("backing up file ",item.path_display, ' to',backupfile)
                        self.dbx.files_download_to_file(backupfile,item.path_display)
                       
                        print("deleting file ",item.path_display )
                        self.PA.dbx.files_delete(item.path_display)
                    
    def MailPlot(self,recipient_list): 
        """will send the plots to people in the email list""" 
        
        with open(recipient_list)  as f:
            Lines = f.readlines()
        b=''
        for line in Lines: 
            a=line.strip()
            if(b != ''):
                b = b +','+a
            else:
                b = a

        subject = ' LCWA speedtest for '+ datetime.datetime.today().strftime('%Y-%m-%d')

        
        
        message = ' this is the daily Raspberry PI report'
        file = self.PA.pdf   
        
        sa = SFM.MyMail(file,b,subject, message)
        from pathlib import Path
        home = str(Path.home())   
         
        sa.send_email_pdf_figs(home+'/private/LCWA/andifile')
    def DoPlotting(self):
        
        temp = 'LC'
        dirlist = []
        for k in range(1,16):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
        token_file = '/git/speedtest/src/LCWA_d.txt'
        tempdir = 'scratch'
        self.PA =PA =PL.PlotAll(token_file,dirlist)
        PA.ConnectDropbox()
        PA.GetFiles()
        PA.PushFileDropbox()
        
    def CreateHistory(self):
        """ reads csv files from different days and then adds them into one large file
        """
        #Again we loop over the different directories
        #first delete all old history files
        delete_cmd ='rm '+str(Path.home()) +'/scratch/*history.txt'  

        os.system(delete_cmd)
        
        temp = 'LC'
        dirlist = []
        for k in range(1,16):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
            
        for k in range(len(dirlist)):
            temp = '/LCWA/'+dirlist[k] # file on dropbox
            print('now working on combining files in  ',temp)

        
            MyDir = self.PA.dbx.files_list_folder(temp)
            for item in MyDir.entries:
                if isinstance(item, dropbox.files.FileMetadata):
                    now = datetime.datetime.now() #determine how old a file is
                    diff = now - item.server_modified #take the difference
                   
                    if(diff.days > 7 ):
                        pass# we are only using 7 days
                    else:
                        #open file, read it , remove first line
                        #make sure that it is a csv file
                        if "csv" in item.path_display:
                            self.ReadFile(dirlist[k]+'history.txt', item.path_display)
                        
       
    def ReadFile(self,file,path_display):    
        
        home = str(Path.home())   
        temp = home+'/scratch/tempfile.txt'
        self.PA.dbx.files_download_to_file(temp,path_display)
        # now read the file , strip firts line and add to summary file
        with open(temp,"r") as f:
            rows = f.readlines()[1:] # strips the first line
        filename = home+'/scratch/'+file
        if os.path.isfile(filename):
            output_file = open(filename,'a')
        else :
            output_file = open(filename,'w')

        output_file.writelines(rows)
        output_file.close()
        
        
       
        
if __name__ == '__main__':
    #create the list
    from pathlib import Path
    home = str(Path.home())   
    recipient_list = home+'/private/LCWA/recipient_list.txt'
    backupdir = home+'/LCWA_backup'
    
    MC = MyControl(backupdir)
    
    #Here we check if we are close to a time window
    timestamp = datetime.datetime.now().time() # Throw away the date information
    start = datetime.time(23, 49)
    end = datetime.time(23,59)
    if(start<timestamp<=end):
        print (start <= timestamp <= end) # >>> depends on what time it is
    
        MC.MailPlot(recipient_list)
    MC.CreateHistory()
