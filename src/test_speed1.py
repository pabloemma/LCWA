#!/usr/bin/env python
### BEGIN INIT INFO for raspi startup
# Provides:          test_speed1.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO



'''
Created on Feb 8, 2020

@author: klein


This is based on the CLI program from speedtest
It basically provides a python wrapper around the speedtest, so that we can fill
the results in a file, which can then be plotted
The original version of test_speed was pabsed on pyspeedtest and gave different results from
the GUI


some notes about the speedtest CLI; In csv mode the output is Bytes/second. In order to get Mbs, 
we have to multiply the output by 8./1e6


 the output format is
 day,time,server name, server id,latency,jitter,package loss in %, download, upload 


For raspi startup we need to
sudo cp test_speed1.py /etc/init.d
sudo update-rc.d test_speed1.py defaults

for espeak on raspi, might have to do pulseaudio -D

'''

import sys
import time
import os
import datetime
import textwrap
from datetime import  date 
import argparse as argp  # we want to use CLI
import platform # need to determine the OS
import subprocess as sp
import dropbox
import socket # needed for hostname id
from __builtin__ import True


class test_speed1():
    
    
    
    def __init__(self,server,chosentime):
        #print (' in init')        # before we do anything, let's determine the python version

        self.chosentime = chosentime # how long to wait in seconds before next reading
          
            
        self.WriteHeader()
        
        self.DropFlag = False # default no dropbox connection
        
        self.Debug = False
        # check if we have espeak
        

#    give an audio signal that program is starting
        if platform.system() == 'Darwin':
            try:
                sp.call('/usr/local/bin/espeak " LCWA speedtest starting on Raspberry Pi"',shell=True)
            except:
                print 'nospeak'
        elif platform.system() == 'Linux':
            try:
                sp.call('/usr/bin/espeak " LCWA speedtest starting on Raspberry Pi"',shell=True)
            except:
                print 'nospeak'
    
    def ConnectDropBox(self):
        """
        here we establish connection to the dropbox account
        """
        #f=open(self.keyfile,"r")
        #self.key =f.readline() #key for encryption
        #self.key = pad(self.key,16)
        #f.close()

        f=open(self.cryptofile,"r")
        self.data =f.readline() #key for encryption
        

         
         
         
         #connect to dropbox
        #self.dbx=dropbox.Dropbox(unpad(cipher.decrypt( enc[16:] ),16))
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))

        self.myaccount = self.dbx.users_get_current_account()
        print('***************************dropbox*******************\n\n\n')
        print self.myaccount.name.surname , self.myaccount.name.given_name
        print self.myaccount.email
        print('\n\n ***************************dropbox*******************\n')
        
        
    def WriteHeader(self):   
        '''
        gives out all the info at startup
        '''
        print(sys.version_info[0])
        if (sys.version_info[0] == 3):
            print(' we have python 3')
            self.vers = 3
            print ('not implemented yet')
            sys.exit(0)
        else:
            print('you are behind the curve with python2')
            self.vers = 2
       
        
        print('\n \n \n')    
        
        print('****************************************************************** \n')   
        print('hello this is the LCWA speedtest version',self.vers)
        print('Written by Andi Klein using the CLI from speedtest')
        print('Run date',datetime.datetime.now()) 
        print('\n ')    
        
        print('****************************************************************** \n')   
        print('\n \n \n')  
        self.Progress()  

    def Progress(self):
        """
        keep track of the updates
        """
        self.vs = '3.04.0'

        
        print(' History')
        print('version 2.02', '  trying to catch the random bad data sent by the CLI')
        print('version 2.03', ' fixed conversion problem for N/A')
        print('        version 2.03.1', ' fixed rasp problem wit -L and -V')
        print('version 3.01.0', 'connect to dropbox and store file every 50 entries')
        print('        3.01.1', 'added header line to output')
        print('version 3.02.0', ' - made cybermesa default server unless requested ')
        print('                     - at midnight we open a new file')
        print('version 3.02.1',' print some info on dropbox')
        print('version 3.02.2',' write dropbox file around the half hour mark')
        print('Version 3.02.3', ' Included a header which is needed for the raspberry pi to start test_speed1 at boot')
        print('                     - gives an acoustic signal at startup')
        print('Version 3.03.0', ' added a Debug switch')
        print('Version 3.04.0', 'get host name and add it to the filename')
        print('\n\n\n')
        
        
    def GetArguments(self):
        """
        this method deals with arguments parsed
        """
        #instantiate the parser
        parser = argp.ArgumentParser(
            prog='test_speed1',
            formatter_class=argp.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''
            Output format:
            day,time,server name, server id,latency[ms],jitter[ms],package loss[%], download Mb/s, updload Mb/s
            If you don't  give a filename for the password and the key, \n
            you will not coinnect to the output
            dropbox 
             
             
             '''))

        
        # now we build up the different args we can have
        parser.add_argument("-s","--serverid",help = "Specify a server from the server list using its id" )
        parser.add_argument("-L","--servers",action='store_true',help = "List nearest servers" )
        parser.add_argument("-V","--version",action='store_true',help = "Print CLI version" )
        parser.add_argument("-o","--host",help = "Specify a server, from the server list, using its host's fully qualified dom" )
        parser.add_argument("-ip","--ip",help = "Attempt to bind to the specified IP address when connecting to servers" )
        parser.add_argument("-t","--time",help = "time between succssive speedtests in minutes (integer)" )
        #parser.add_argument("-p","--pwfile",help = "The passwordfile" )
        parser.add_argument("-d","--dpfile",help = "The file for the dropbox" )
        parser.add_argument("-a","--adebug",action='store_true',help = "a debug version" )

        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        
        
        
        #list of argument lists
        
        
    
        # here some of the defaults
        #Of courss Mac has the stuff in different places than Linux
        if platform.system() == 'Darwin':
            temp1=["/usr/local/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default
        elif platform.system() == 'Linux':
            temp1=["/usr/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default         
        # do our arguments
        else:
            print' Sorry we don\'t do Windows yet'
            sys.exit(0)
        args = parser.parse_args()
        #check if there are any arguments
        
        
        self.loop_time = 60 # default 1 minutes before next speedtest
        
        if(len(sys.argv) == 1):
            # we need to give it a server as default use cyber mesa
            se =['-s','18002']
            temp1.extend(se)
            self.command = temp1
            #self.keyfile('LCWA_p.txt')
            return
        else:
            if(args.adebug):
                self.ARGS = sys.argv
                self.DebugProgram(1)
                self.Debug = True
                self.Prompt = 'Test_speed1_Debug>'
            #make cyber mesa the default
            if(args.servers):
                if platform.system() == 'Darwin':

                    self.command = ["/usr/local/bin/speedtest", '-L'] #because argparse does not take single args
                elif platform.system() == 'Linux':
                    self.command=["/usr/bin/speedtest",'-L'] # we want csv output by default         
                   
                
                self.RunShort()
                sys.exit(0)
            if(args.version):
                if platform.system() == 'Darwin':

                    self.command = ["/usr/local/bin/speedtest", '-V'] #because argparse does not take single args
                elif platform.system() == 'Linux':
                    self.command=["/usr/bin/speedtest",'-V'] # we want csv output by default         
                
                self.RunShort()
                sys.exit(0)
                
            if(args.serverid != None):
                t=['-s',args.serverid]
                temp1.extend(t)
            else: # make cybermesa the default
                t=['-s','18002']
                temp1.extend(t)
              
            

            if(args.ip != None):
                t=['--ip=',args.ip]
                temp1.extend(t)
                
            if(args.host != None):
                t=['--host=',args.host]
                temp1.extend(t)
            if(args.time != None):
                self.loop_time = int(args.time)*60 # time between speedtests
                
            #if(args.pwfile != None ) and (args.dpfile != None):
            if(args.dpfile != None):
                #self.keyfile = args.pwfile
                self.cryptofile = args.dpfile
                self.DropFlag = True
                self.ConnectDropBox() # establish the contact to dropbox
                
        self.command = temp1 
        if(self.Debug):
            self.DebugProgram(2)     
        return 
    
    def RunLoop(self):
        """
        calls run and forms the loop
        """
        counter = 0
        
        
        
        while(1):
            self.Run()
            if(self.ConnectDropBox):
                counter = counter + 1
            
                #if (counter==50):
                if( self.WriteTimer()):
                    # we write always around xx:30 
 
                    
                    
                    
                    f =open(self.lcwa_filename,"rb")
                    self.dbx.files_upload(f.read(),'/LCWA/'+self.docfile,mode=dropbox.files.WriteMode('overwrite', None))
                    print('wrote dropbox file')
                    counter = 0 

            time.sleep(self.loop_time)

            
    def WriteTimer(self):
        """
        determines the time
        so that we fill the dropbox file every hour
        """ 
        
        #determine the current time
        b=  datetime.datetime.now()
        #fill in tuple
        a=b.timetuple()
        # this is really a structure with 
        # a.tm_hour
        # a.tm_min
        # a.tm_sec the various elements
        # we want to make sure that our a.tm_min is between in a window around 30 minutes
        # given by self.loop_time, which is in seconds
        temp = int(self.loop_time/60.)
        if(temp < 2): temp =2
        temp = temp/2
        # if we get negative time, that means we sleep longer than 60 minutes
        if(30 - temp <0): 
            return True # this way we write whenever we did a speedtest
        # then we should just continue to write always at x:30
        # now comes the test
        if( a.tm_min > 30 - temp) and ( a.tm_min < 30 + temp):
            return True
        else:
            return False
        
        
        
        
            
    def RunShort(self):    
        process = sp.Popen(self.command,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         universal_newlines=True)
        
        out,err = process.communicate()
        
        print out
        sys.exit(0)
            
                    
    def Run(self):
        """
        this is the heart of the wrapper, using the CLI command
        """
        
        #print self.command
        process = sp.Popen(self.command,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         universal_newlines=True)
        
        out,err = process.communicate()
        
        a=str(out)
        #a is now a tuple , which we fill into a csv list
        self.CreateOutput(a)
        
        if(self.Debug):
            self.DebugProgram(5)
        

        myline=''
        # now create outputline from tuple
        for k in range(len(self.output)-1):
            myline=myline+str(self.output[k])+','
        myline = myline+str(self.output[len(self.output)-1])+'\n'

        
        #check for date, we will open new file at midnight
        if(date.today()>self.current_day):
                #we have a new day
            self.output_file.close()
            self.OpenFile()

        
        if(self.Debug):
            self.myline = myline
            self.DebugProgram(3)
        print myline
        self.output_file.write(myline)
        
        
    def CreateOutput(self,inc1):
        """
        this takes the output line tuple and creates the csv line for the outputfile
        """
        #start with trhe current time and date
        now=datetime.datetime.now()
        
        self.output = [now.strftime("%d/%m/%Y"),now.strftime("%H:%M:%S")]
        
        # strip ,NM out of the server description
        
        #First rempve all double quotes
        tt=inc1.replace('"','')
        inc=tt.split(',')

        # cehck data integrity
        if(len(inc) < 2):
            print('bad data block')
            return
        if(len(inc) != 11):
            print('bad block length')
            return
        
        
        if(self.Debug):
            self.inc = inc
            self.DebugProgram(4)
        self.output.append(inc[0])
        self.output.append(int(inc[2]))
        for k in  [3,4,5]:
            try:
                float(inc[k])
                self.output.append(float(inc[k]))
            except ValueError:
                print('bad int conversion')
                self.output.append(-10000.)
            
            
        for k in  [6,7] :
            try:
                float(inc[k])
            
                self.output.append(float(inc[k])*8./1000000)
            except ValueError:
                print('bad float conversion')
                self.output.append(-999.)
                
            
        return 


    def OpenFile(self):
        ''' the default filename is going to be the date of the day
        and it will be in append mode
        '''
        self.current_day = date.today()
        a = datetime.datetime.today().strftime('%Y-%m-%d')
        self.GetIPinfo()
        filename =self.hostname + a+'speedfile.csv'  #add hostname
        # if filename exists we open in append mode
        #otherwise we will create it
        homedir = os.environ['HOME']
        self.docfile = filename #filename for dropbox
        filename = homedir + '/speedfiles/'+filename
        print filename
        self.lcwa_filename = filename
        if os.path.isfile(filename):
            self.output_file = open(filename,'a',0)
        else :
            self.output_file = open(filename,'w',0)
            self.WriteOutputHeader() # first time we write a header
            
            
    def WriteOutputHeader(self):       
        """
        Write the header for the output file
        """
        Header = 'day,time,server name, server id,latency,jitter,package , download, upload \n'
        self.output_file.write(Header)
        
    def DebugProgram(self,err): 
        """
        Debug statements
        """
        temp = 'test_speed1_debug> '
        if(err == 1) :
            for k in range(len(self.ARGS)):
                print temp,' cli commands',self.ARGS[k]
        elif(err ==2):
            print temp, 'command for program ', self.command 
        elif(err ==3): 
            print temp, 'Output :'
            print self.myline
        elif(err == 4):
            print temp,'Data block',self.inc
        elif(err == 5):
            print temp,' output',self.output  #for debugging
        elif(err==6):
            print temp ,' my hostname ',self.hostname
            print temp , 'my IP is '  , self.my_ip 
            
    def GetIPinfo(self):
        """
        gets the host info
        """
        a = socket.gethostname()
        self.my_ip = socket.gethostbyname(a)
        
        # now chek the hostname if it is >4 characters strip rest
        # if it is shorter pad
        if len(a) > 4:
            self.hostname = a[:4]+'_'
            
        elif len(a) < 4:
            temp='xxxx'
            
            self.hostname = a+temp[0:4-len(b)]+'_' #pad with xxxx
        else:
            self.hostname = a+'_'
        
        if(self.Debug):
            self.DebugProgram(6)
        
        return
        
if __name__ == '__main__':
    
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed1(server=server1,chosentime=60)
    ts.GetArguments()  #commandline args
    ts.OpenFile()  #output file
    
#    ts.GetArguments()
#    ts.OpenFile()
    ts.RunLoop()

    pass
