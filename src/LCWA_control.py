'''
Created on Apr 24, 2020

@author: klein
'''

import PlotAll as PL
import dropbox
import datetime


class MyControl(object):
    '''
    this class runs plotall and does some housekeeping at dropbox
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
        #first get everything setup with dropbox by excuting DoPlotting
        
        self.DoPlotting()
        
        self.CleanupDropbox()
        
        
        
    def CleanupDropbox(self):
        """
        Here we go into the dropbox directories and check for old files (older than a week)
        """
        
        
        #loop over directories and check if anyone has something older than one week
        
        
        MyDir = self.PA.dbx.files_list_folder('/LCWA/ROTW',recursive=True)
        
        for item in MyDir.entries:
            if isinstance(item, dropbox.files.FileMetadata):
                now = datetime.datetime.now() #determine how old a file is
                diff = now - item.server_modified #take the difference
                if(diff.days > 8 ):
                    print ('name = ' , item.name)
                    print ('path  = ', item.path_display )
                    print ('fileID = ' , item.id)
                    print ('date = ', item.server_modified)
                    # here we delete the files
                    print("deleting file ",item.path_display )
                    self.PA.dbx.files_delete(item.path_display)
                    
                 
    
    def DoPlotting(self):
        
        temp = 'LC'
        dirlist = []
        for k in range(1,16):
            if (k<10):
                temp1 = temp+'0'+str(k)+'_'
            else:
                temp1 = temp+str(k)+'_'
            
            dirlist.append(temp1)
        token_file = '/Users/klein/git/LCWA/src/LCWA_d.txt'
        tempdir = 'scratch'
        self.PA =PA =PL.PlotAll(token_file,dirlist)
        PA.ConnectDropbox()
        PA.GetFiles()
        PA.PushFileDropbox()
        
if __name__ == '__main__':
    #create the list
    MC = MyControl()
