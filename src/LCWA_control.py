'''

Created on Apr 24, 2020

@author: klein
more changes test of git
'''
 
import PlotAllNew as PL  # new plot routine
import MakePlots as MP
import dropbox
import datetime
import SendFileMail as SFM
import os
import datetime
from pathlib import Path


 
class MyControl(object):
    '''
    this class runs plotall and does some housekeeping at dropbox
    '''


    def __init__(self, backupdir,debug=False, report_date = None):
        '''
        Constructor
        '''
        
        
        #first get everything setup with dropbox by excuting DoPlotting
        
        #introduce new variable debug and report_date
        #this allows to select a specific date ro report on and only send the email to
        #me , so I don't bombard everyboddy with emails, while I am trying to figure ourt where I fucked up.
        self.debug = debug
        self.report_date = report_date
 
        self.low_range = 1
        self.hi_range = 25  # number of boxes we have out +1

        # determine the home path and set accordingly
        self.myhome_path = Path.home()
        
        self.backupdir = backupdir
        
        self.DoPlotting()
        
        self.CleanupDropbox()


 
        
        #initialize the Makeplots class
        
        self.MP1 = MP.MakePlots()
        
        
    def CleanupDropbox(self):
        """
        Here we go into the dropbox directories and check for old files (older than a week)
        """
        
        
        #loop over directories and check if anyone has something older than one week
        temp = 'LC'
        dirlist = []
        for k in range(self.low_range,self.hi_range):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
            
        for k in range(len(dirlist)):
            temp = '/LCWA/'+dirlist[k] # file on dropbox
            #print('now checking ',temp)

        
            MyDir = self.PA.dbx.files_list_folder(temp) #do NOT use recursive, since that does not work for shared folders
        
            for item in MyDir.entries:
                #print("item",item,' ',MyDir.entries)
                if isinstance(item, dropbox.files.FileMetadata):
                    now = datetime.datetime.now() #determine how old a file is
                    #print('hallelujah',temp,'  ',item.name, '  ',item.server_modified)
                    diff = now - item.server_modified #take the difference
                    print('difference in days',diff.days)
                    print(now,item.server_modified)
                    #if diff.days == 1 or  diff.days == 2 or  diff.days == 3:  # changed to or so that we backup the last 2 days
                    if diff.days >= -1:  # changed to or so that we backup the last 2 days
                        print ('name = ' , item.name)
                        print ('path  = ', item.path_display )
                        print ('fileID = ' , item.id)
                        print ('date = ', item.server_modified)
                    # here we backup and delete the files
                        backupfile = self.backupdir+item.name
                        #print("backing up file ",item.path_display, ' to',backupfile)
                        try:
                            a = self.PA.dbx.files_download_to_file(backupfile,item.path_display)
                            #print("return type ",a)
                        except:
                            print("problems with backing up ",item.path_display )
                        if(diff.days > 4 ):  # changed to -1 so that we backup every day
 
                            #print("deleting file ",item.path_display )
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

        
        
        #message = ' this is the daily Raspberry PI report, \n blue is download green upload, \n \
        # \n  \n'  
        message = ' If you want to continue to get the daily Raspberry PI report, \n please send me an email at \
        : \n pabloemma@gmail.com by 14th of April \
         \n  \n'

        file = self.PA.pdf   
        
        sa = SFM.MyMail(file,b,subject, message)
        
        home = str(self.myhome_path)   
         
        sa.send_email_pdf_figs(home+'/private/LCWA/andifile')

    def MailPlotNew(self,recipient_list):
        """new version, using nash script"""
        with open(recipient_list)  as f:
            Lines = f.readlines()
        b=''
        for line in Lines: 
            a=line.strip()
            if(b != ''):
                b = b +','+a
            else:
                b = a

        subject = ' LCWA_speedtest_'+ datetime.datetime.today().strftime('%Y-%m-%d')
        #subject = " \"Ignore previous data set, this is the set for 12-23-2023 \" "

        
        message = ' this_is_the_daily_Raspberry_PI_report ' #this is actually done in message.txt
        
        #message = ' this_is_the_daily_Raspberry_PI_report for 12-23-2023, ignore previous one'

        file = self.PA.pdf  

        # create mail command
        if(self.debug):
            mail_command = str(self.myhome_path)+'/git/speedtest/src/mail_test_debug.sh '+file+' '+subject+' ' + str(self.myhome_path)+'/git/speedtest/src/message.txt'
        else:   
            #mail_command = '/home/klein/git/speedtest/src/mail_test.sh '+file+' '+subject+' ' + '/home/klein/git/speedtest/src/message.txt'
            mail_command = str(self.myhome_path)+'/git/speedtest/src/mail_test.sh '+file+' '+subject+' ' + str(self.myhome_path)+'/git/speedtest/src/message.txt'
        print(mail_command)
        os.system(mail_command)  
        return      




    def DoPlotting(self):
        
        temp = 'LC'
        dirlist = []
        for k in range(self.low_range,self.hi_range):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
        #dirlist = ['LC15_']
        token_file = '/git/speedtest/src/LCWA_a.txt'
        #tempdir = 'scratch'
        if(self.debug):

            self.PA =PA =PL.PlotAll(token_file,dirlist,filedate = self.report_date)
            #self.PA =PA =PL.PlotAll(token_file,dirlist,filedate = '2023-12-10')
        else:
            self.PA =PA =PL.PlotAll(token_file,dirlist,filedate = self.report_date)

        PA.ConnectDropBox()
        PA.GetFiles() 
        PA.PushFileDropbox()

        
       
        
    def CreateHistory(self):
        """ reads csv files from different days and then adds them into one large file
        """
        #Again we loop over the different directories
        #first delete all old history files
        delete_cmd ='rm '+str(self.myhome_path) +'/scratch/*history.csv'  

        os.system(delete_cmd)
        
        temp = 'LC'
        dirlist = []
        for k in range(self.low_range,self.hi_range):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
            
        self.dirlist = dirlist    
        for k in range(len(dirlist)):
            temp = '/LCWA/'+dirlist[k] # file on dropbox
            print('now working on combining files in  ',temp)

        
            MyDir = self.PA.dbx.files_list_folder(temp)
            for item in MyDir.entries:
                if isinstance(item, dropbox.files.FileMetadata):
                    now = datetime.datetime.now() #determine how old a file is
                    diff = now - item.server_modified #take the difference
                    
                    if(diff.days > 4 ):
                        pass# we are only using 7 days
                    else:
                        #open file, read it , remove first line
                        #make sure that it is a csv file
                        if "csv" in item.path_display:
                            self.ReadFile(dirlist[k]+datetime.datetime.today().strftime('%Y-%m-%d')+'history.csv', item.path_display)
        return           
       
    def ReadFile(self,file,path_display):    
        
        home = str(self.myhome_path)   
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
        
    def PlotHistory(self):  
        """
        plot the history file
        """
       
        for k in range(len(self.dirlist)):
       
       
            file = str(self.myhome_path)+'/scratch/'+self.dirlist[k]+datetime.datetime.today().strftime('%Y-%m-%d')+'history.csv'   
            print('plotting history file  ' ,file)

            if os.path.isfile(file):
            
                self.MP1.ReadCSVFile(file) 
                self.MP1.MakeThePlots()
                self.PushFileDropbox(k)
            else:
                pass
    def PushFileDropbox(self,k):  
        
        f = open(str(self.myhome_path)+'/scratch/'+self.dirlist[k]+datetime.datetime.today().strftime('%Y-%m-%d')+'history.pdf',"rb") 
        dropdirfile = '/LCWA/'+self.dirlist[k]+'/'+self.dirlist[k]+datetime.datetime.today().strftime('%Y-%m-%d')+'history.pdf'
        self.PA.dbx.files_upload(f.read(),dropdirfile,mode=dropbox.files.WriteMode('overwrite', None))
 
        
if __name__ == '__main__':
    #create the list
    debug = False
    #report_date = '2024-04-11'
    report_date = None  # use this for norma run
    from pathlib import Path
    # next we get current time so that we can calculate how long the program took
    prog_start_time = datetime.datetime.now()
    home = str(Path.home())   
    recipient_list = home+'/private/LCWA/recipient_list.txt'
    recipient_list_short = home+'/private/LCWA/recipient_list_short.txt'
    backupdir = home+'/LCWA_backup/'
    if(debug):
        MC = MyControl(backupdir,debug=debug,report_date=report_date)
    else:
        MC = MyControl(backupdir,report_date=report_date)
    
    #Here we check if we are close to a time window
    timestamp = datetime.datetime.now().time() # Throw away the date information
    start = datetime.time(23, 49)
    end = datetime.time(23,59)
    # for a different date use the line 132
    start = datetime.time(1,25)
    end = datetime.time(23,59)
    if(start<timestamp<=end):
        print (start <= timestamp <= end) # >>> depends on what time it is
    
        #MC.MailPlot(recipient_list)
        if(debug):
            MC.MailPlotNew(recipient_list_short)
        else:
            MC.MailPlotNew(recipient_list)
           
    MC.CreateHistory()
    MC.PlotHistory()
    prog_end_time = datetime.datetime.now()
    time_used = prog_end_time - prog_start_time 
    print('\n \n It took the program ',time_used.total_seconds(),' to complete')                                                                                                                                      
    #MC.PlotHistory()
