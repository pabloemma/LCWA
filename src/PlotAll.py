'''
Created on Apr 21, 2020

@author: klein

Gets all the csv files from the different directories and plots them
'''



import dropbox

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
    token_file = '/Users/klein/git/speedtest/src/LCWA_d.txt'

    PA=PlotAll(token_file,dirlist)
    PA.ConnectDropbox()