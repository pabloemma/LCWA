#!/usr/bin/env python3
### BEGIN INIT INFO for raspi startup
# Provides:          test_speed1.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
#from builtins import True
# this is temprary new version 2_0 which has a switch between iperf and speedtest every 
# 10 minutes

  

'''
Created on Feb 8, 2020

@author: klein
   

This is based on the CLI program from speedtest
It basically provides a python wrapper around the speedtest, so that we can fill
the results in a file, which can then be plotted
The original version of test_speed was basesed on pyspeedtest and gave different results from
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
from tarfile import BLOCKSIZE
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
import PlotClass as PC # new plot version
import uuid
import ntplib
import random

from tcp_latency import measure_latency

import iperf_client as ipe
import config_speed as cs
import set_time_gh as st

#from __builtin__ import True


class test_speed1():
    
    
    
    def __init__(self,server,chosentime):
        #print (' in init')        # before we do anything, let's determine the python version

        self.chosentime = chosentime # how long to wait in seconds before next reading

         # here we read in the configuration file
         # first we locate where the directory with test_speed1_3 py is located
         # the configuration file is then  at ../config
        
          
            
        self.WriteHeader()
        
        #self.DropFlag = False # default no dropbox connection
        
        #self.Debug = False
        
       
        self.GetMacAddress()
        #self.Setup() # now done ir agrparse
        # here we wait for the program to start until we rach the time

    def QueueRuntime(self):                                              # WGH Mod: Allows for skipping the wait queue via cmdline arg
        
        # here we wait for the program to start until we reach the time
        MyT = st.MyTime()
        success = MyT.GetTime()
        
        # Only initiate the wait queue if our loop_time is 10 minutes or greater..
        if self.loop_time > 599 and not self.nowait:
            print("Queueing test wait time..")
            host = socket.gethostname()
            if success:
                if(host[0:2] == 'LC'):
                    MyT.SetStart(host)
                else:
                    MyT.SetStart('LC00')
            else:
                self.Logging('Could not connect to ntp server')
        else:
            print("Jumping test wait queue..")
        
        




    def Setup(self, config_file = None  ):
        """" checks for systerm version and sets some path
        The deafult is the config file created from the program """
        
        #lets get the python interpreter"
        self.python_exec = sys.executable
        self.myplatform = platform.system()

        # lets get the config file

        
        workdir = os.path.dirname(os.path.abspath(__file__))
        confdir = workdir.replace('src','config')

        # chek if we run it as a service
        # because of Gordon's wishes, but now we firts have to
        #check it is not a mac: If it is a mac the config file is at its usual point
        # if linux, it depends how the machine is setup
        if(self.myplatform == 'Darwin'):
            if config_file == None :
                config_file = confdir+'/test_speed_cfg.json'
                MyConfig = cs.MyConfig(config_file)
            else:
                        
                MyConfig = cs.MyConfig(config_file)

        else:
            if config_file == None :
                
                status = os.system('systemctl is-active --quiet lcwa-speed*')
                if(status == 0):
                    print('we are running the program under systemd',status)  # will return 0 for active else inactive.    
                    confdir = '/etc/lcwa-speed/'
                    config_file = confdir+'/lcwa-speed.json'
 
                    MyConfig = cs.MyConfig(config_file)
 
                else:
                    config_file = confdir+'/test_speed_cfg.json'

                    MyConfig = cs.MyConfig(config_file)
            else:
                if(config_file[0] =='/'): #it already has full path in it
                   MyConfig = cs.MyConfig(config_file) 
                else:
                    MyConfig = cs.MyConfig(confdir+'/'+config_file)
            

        
        
        self.timeout_command = MyConfig.timeout #where the system has the timeout
        self.speedtest_srcdir = MyConfig.srcdir # the src dir where all the routines are
        self.runmode = MyConfig.runmode         #ookla or iperf
        self.Debug = MyConfig.debug
        self.cryptofile = MyConfig.cryptofile
        

        

        if (self.runmode == 'Iperf'):
        #iperf variables
            self.iperf_server =     MyConfig.iperf_serverip
            self.iperf_port =       MyConfig.iperf_serverport
            self.iperf_duration =   MyConfig.iperf_duration
            self.iperf_blksize =    MyConfig.iperf_blksize
            self.iperf_numstreams = MyConfig.iperf_numstreams
            self.iperf_reverse    = MyConfig.iperf_reverse
            self.loop_time =        MyConfig.time_window*60
            
        elif(self.runmode == 'Speedtest'):

            self.latency_server =   MyConfig.latency_ip
            self.serverid =         MyConfig.serverid
            self.serverip =         MyConfig.serverip
            self.latency_server =   MyConfig.latency_ip
            self.loop_time =        MyConfig.time_window*60
            self.speedtest =        MyConfig.speedtest     # location of the Ookla speedtest

       
        elif(self.runmode == 'Both'):
            self.iperf_server =     MyConfig.iperf_serverip
            self.iperf_port =       MyConfig.iperf_serverport
            self.iperf_duration =   MyConfig.iperf_duration
            self.iperf_blksize =    MyConfig.iperf_blksize
            self.iperf_numstreams = MyConfig.iperf_numstreams
            self.iperf_reverse    = MyConfig.iperf_reverse
            self.latency_server =   MyConfig.latency_ip
            self.serverid =         MyConfig.serverid
            self.serverip =         MyConfig.serverip
            self.latency_server =   MyConfig.latency_ip
            self.loop_time =        MyConfig.time_window*60
            self.speedtest =        MyConfig.speedtest     # location of the Ookla speedtest
            self.click      =       MyConfig.click # this is a flip flop of values
            self.random_click =     MyConfig.random_click # if 1 the program determines randomly to to iperf or speedtest
 
        else:
            self.Logging('Unknown runmode')
            sys.exit(0)
                

    
    def ConnectDropBoxOld(self):
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
        print( self.myaccount.name.surname , self.myaccount.name.given_name)
        print (self.myaccount.email)
        print('\n\n ***************************dropbox*******************\n')
       
    def ConnectDropBox(self):
        """
        here we establish connection to the dropbox account
        """
        print("at connect dropbox")
        self.TokenFile=self.cryptofile.strip('\n')
        #f=open(self.TokenFile,"r")

        # now we branch out depending on which keyfile we are using:
        if  'LCWA_d.txt' in self.TokenFile:
            print("old system")
            f=open(self.TokenFile,"r")
            self.data =f.readline() #key for encryption
        

         
         
         
         #connect to dropbox 
            self.dbx=dropbox.Dropbox(self.data.strip('\n'))
            print("self.dbx",self.dbx)

 
        elif 'LCWA_a.txt'  in self.TokenFile:
            print('new system')
            f=open(self.TokenFile,"r")
  
            temp =f.readlines() #key for encryption
            temp_buf = []
  
            for k in range(len(temp)):
                temp1 = temp[k].strip('\n')
                start   = temp1.find('\'') # find beginning quote
                end     = temp1.rfind('\'') # find trailing  quote
                temp_buf.append(temp1[start+1:end])
        
        


        
    
             #connect to dropbox 
            #self.dbx=dropbox.Dropbox(self.data.strip('\n'))
            APP_KEY = temp_buf[0]
            APP_SECRET = temp_buf[1]
            REFRESH_TOKEN = temp_buf[2]

            



            self.dbx = dropbox.Dropbox(
                app_key = APP_KEY,
                app_secret = APP_SECRET,
                oauth2_refresh_token = REFRESH_TOKEN
                )
            print("self.dbx",self.dbx)

        
        else:
            print("wrong keyfile")


        

        self.myaccount = self.dbx.users_get_current_account()
        print('***************************dropbox*******************\n\n\n')
        print( self.myaccount.name.surname , self.myaccount.name.given_name)
        print (self.myaccount.email)
        print('\n\n ***************************dropbox*******************\n')
        self.ConnectDropBox_ok = True
        return self.dbx

         
         
         
         
        
    def WriteHeader(self):   
        '''
        gives out all the info at startup
        '''
        print(sys.version_info[0])
        if (sys.version_info[0] == 3):
            print(' we have python 3')
            self.vers = 3
            #print ('not implemented yet')
            #sys.exit(0)
        else:
            print('you are behind the curve with python2')
            self.vers = 2
       
        
        print('\n \n \n')    
        start = "\033[1m"
        stop = "\033[0m"

        print('****************************************************************** \n')   
        print('hello this is the LCWA speedtest version',self.vers)
        print('Written by Andi Klein using the CLI from speedtest')
        print('Run date',datetime.datetime.now(),'\n') 
        print('Running from ' , self.DigIP() )
        print('\n ')    
        
        print('****************************************************************** \n')   
        print('\n \n \n')  
        self.Progress()  

    def Progress(self):
        """
        keep track of the updates
        """
        self.vs = '8.02.02'
 
        
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
        print('Version 4.00.0', 'runs on python3 now')
        print('Version 5.00.0', 'automatically does plots and ships them to dropbox')
        print('Version 5.01.0', 'new dropbox configuration')
        print('Version 5.01.1', 'added lookup of ip address')
        print('Version 5.01.2', 'stop at 23:45 to 24:00, flush data and exit')
        print('Version 5.01.3', 'Create textfile with important values')
        print('Version 5.01.4', 'test of distro')
        print('Version 5.01.5', 'timestamp in log file')
        print('Version 5.01.6', 'added close_fds=True to popen')
        print('Version 5.01.7', 'added using timeout command')
        print('Version 5.01.8', 'better error message')
        print('Version 5.01.9', 'date and time output')
        print('Version 5.01.10', 'catching network problems')
        print('Version 5.01.11', 'force LC12 to connect to NMSURF, done in the arg parse section')
        print('Version 5.01.12', 'force LC24 to connect to NMSURF, done in the arg parse section')
        print('Version 6.00.01', 'now with latency measurement to currently cybermese')
        print('Version 6.00.02', 'minor change in PlotCalss do do the scaling on the single pdf files better')
        print('Version 7.00.01', 'major upgrade , replace speetetst with iperf')
        print('Version 7.01.02', 'added config file')
        print('Version 7.01.03', 'added Gordon wish for /etc location for config file')
        print('Version 7.01.04', 'Revamped command line and arparse section')
        print('Version 7.01.05', 'added a call to ntp server, start of syncing the speedboxes')
        print('Version 7.01.06', 'add a line to txt file to write runmode')
        print('Version 7.02.01', 'modfy code such that it now reads in a second file to determine what host is running what ')
        print('Version 8.01.01', 'Code which allow you to switch between speedtest and iperf either pretermined or random ')
        print('Version 8.01.02', 'replace server name with speedtest in output csv file ')
         
        print('Version 8.02.01', 'now better reflection on what is going on with iperf, and new more granular config file treatment ')
        print('Version 8.02.02', 'with Gordon time mods ')
        print('Version 8.02.03', 'added an try clause in create iperf output to catch connection problems')
        print('Version 9.00.01', 'new dropbox')
        
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
           day,time,server name, server id,latency[ms],jitter[ms],package loss[%], download Mb/s, updload Mb/s’*

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
        parser.add_argument("-l","--latency",help = "the ip addresss of the latency server" )
        parser.add_argument("-ipf","--iperf",help = "the ip addresss of the iperf  server , format =xx.xx.xx.xx" )
        parser.add_argument("-ipfd","--iperf_duration",help = "the duration of the iperf" )
        parser.add_argument("-c","--conf",help = "the full path of the configuration file" )
        parser.add_argument("-n","--nowait",action='store_true',help = "Disables startup test time wait queueing" )        # WGH mod: skip wait queue for debugging purposes
        parser.add_argument("-w","--testdb",action='store_true',help = "Posts to dropbox immediately" )                    # WGH mod: test dropbox posting immediatly for debugging purposes
        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        

             


         
        #list of argument lists
        #_AK self.run_iperf = True #default
        
        args = parser.parse_args()
        #check if there are any arguments
        #first we check if config file is determend by commandline
        if(args.conf != None):
            self.Setup(args.conf)
        else:
            self.Setup()
 


        #chekc if we run the ookla or iperf version, temp1 is speedtest, temp2 is iperf
        if self.runmode == 'Speedtest' or self.runmode == 'Both':
            temp1=[self.timeout_command,"-k","300","200",self.speedtest,"--progress=no","-f","csv"] # we want csv output by default
        if self.runmode == 'Iperf' or self.runmode == 'Both':
            temp2 =[self.timeout_command,"-k","300","200",self.python_exec,self.speedtest_srcdir+"iperf_client.py"]
        
     
    
       
        
 
        #if no cli args then everything comes from the config file
        # this means that we need to get all the variables defined here
        # Since they have different length we need to make sure we handle all of them.
        # For the Ookla version we need to have the following variables define:
        # serverid : 18002,NMSURF or whatever
        # timewindow: time inetravl for testing
        # latency_ip: the ip of the latency server
        
 
        if self.Debug:
            self.DebugProgram(1)
                
            self.Prompt = 'Test_speed1_Debug>'

 
 
     
        if(args.adebug):
            self.ARGS = sys.argv
            self.DebugProgram(1)
            self.Debug = True
            self.Prompt = 'Test_speed1_Debug>'
            #make cyber mesa the default

        if(args.dpfile != None):
            self.cryptofile = args.dpfile
            if(self.cryptofile[0] == 'L'): # need to add the system path
                self.cryptofile = self.speedtest_srcdir + self.cryptofile
 
            #self.DropFlag = True
            self.ConnectDropBox() # establish the contact to dropbox
        
        #In case we have also None in the config file
        if (args.dpfile == None and self.cryptofile == None):
            self.Logging('You need to provide path for cryptofile, will not connect to dropbox')

        if(self.cryptofile[0] == 'L'): # need to add the system path
            self.cryptofile = self.speedtest_srcdir + self.cryptofile
            self.ConnectDropBox() # establish the contact to dropbox
        else:
            self.ConnectDropBox()
 
        if(args.time != None):
                self.loop_time = int(args.time)*60 # time between speedtests

        if(args.nowait):
            self.nowait = True
        else:
            self.nowait = False

        if(args.testdb):
            self.testdb = True
        else:
            self.testdb = False

 
        if self.runmode == 'Speedtest' or self.runmode == 'Both':

        # here is the block for speedtest    
            if(args.servers):
 
                self.command_speed = [self.timeout_command,"-k","300","200",self.speedtest, '-L'] #because argparse does not take single args
                  
                
                self.RunShort()
                sys.exit(0)
            if(args.version):
                

                self.command_speed = [self.timeout_command,"-k","300","200",self.speedtest, '-V'] #because argparse does not take single args
                
                self.RunShort()
                sys.exit(0)
                
            if(args.serverid != None):
            #if(socket.gethostname() == 'LC12'):
             #   t=['-s','9686']    # go to NMSURF  
             # 
                          
            #else:
                t=['-s',str(args.serverid)]
            
                temp1.extend(t)
            else: # make cybermesa the default
 
                t=['-s',str(self.serverid)]
                temp1.extend(t)
              
            

            if(args.ip != None):
                t=['--ip=',args.ip]
                temp1.extend(t)
        
            if(args.latency != None):
                t=['--latency=',args.latency]
                self.latency_server =  args.latency
            else: #default is cybermesa  
                t=['--latency=','65.19.14.51'] 
                self.latency_server =  '65.19.14.51'

            if(args.host != None):
                t=['--host=',args.host]
                temp1.extend(t)
 
        if self.runmode == 'Iperf' or self.runmode == 'Both' :
            if(args.iperf != None):
                print('running iperf version, setting up iperf')
                self.iperf_server = args.iperf
                t=['-s',self.iperf_server]
                temp2.extend(t)

            if(args.iperf_duration != None):
                self.iperf_duration = int(args.iperf_duration)
            else:
                t=['-d',str(self.iperf_duration)]
                temp2.extend(t)
   
            # add option from config file
            t = ['-n',str(self.iperf_numstreams)]
            temp2.extend(t)

            #blocksize
            t= ['-b',int(self.iperf_blksize)]

            if(self.iperf_reverse):
                t = ['-r']
                temp2.extend(t)



            #if(args.pwfile != None ) and (args.dpfile != None):

            
 
        #form command


        if self.runmode == 'Speedtest':
            self.command_speed = temp1 
        elif self.runmode == 'Iperf':
            temp2.extend(["-s",self.iperf_server])


            self.command_iperf = temp2

        elif self.runmode == 'Both':
            self.command_speed = temp1 
            temp2.extend(["-s",self.iperf_server])

            self.command_iperf = temp2
      
 



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
            if(self.ConnectDropBox_ok):
                counter = counter + 1
            
                #if (counter==50):
                if self.WriteTimer() or self.testdb and not self.FlushTime():                   # WGH mod: test dropbox posting immediatly for debugging purposes
                    # we write always around xx:30 
 
                    
                    
                    
                    f =open(self.lcwa_filename,"rb")
                    print (self.dropdir, '   ',self.docfile)
                    try:
                        self.dbx.files_upload(f.read(),self.dropdir+self.docfile,mode=dropbox.files.WriteMode('overwrite', None))
                        now=datetime.datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        print(dt_string,'   wrote dropbox file')
                    # write textfile
                        self.WriteDescriptor()
                        self.docfile1 = self.docfile.replace('csv','txt')
                        f1=open(self.textfile,"rb")
                        self.dbx.files_upload(f1.read(),self.dropdir+self.docfile1,mode=dropbox.files.WriteMode('overwrite', None))
    
                        if(counter > 0):
                            print (' now saving plotfile')
                            self.DoPlots(textflag = False)
                    except:
                        self.Logging(' Cannot connect to dropbox, will try in 10 minues again')

                        time.sleep(10*60)
                    #counter = 0 
                elif self.FlushTime(): # It is close to midnight, we flush the last file and exit to ensure we laod trhe latest software
                    try:
                        f =open(self.lcwa_filename,"rb")
                        print (self.dropdir, '   ',self.docfile)
                        self.dbx.files_upload(f.read(),self.dropdir+self.docfile,mode=dropbox.files.WriteMode('overwrite', None))
                        self.WriteDescriptor()
                        self.docfile1 = self.docfile.replace('csv','txt')
                        now=datetime.datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        print (dt_string,' now saving plotfile')
                        self.DoPlots(textflag =True)
                        f1=open(self.textfile,"rb")
                        self.dbx.files_upload(f1.read(),self.dropdir+self.docfile1,mode=dropbox.files.WriteMode('overwrite', None))
                        print('midnight exiting')
                        sys.exit(0)
                    except:
                        self.Logging('Midnight save aborted due to network problem')
                        sys.exit(0)
                        
                    #counter = 0 
                    
 
            time.sleep(self.loop_time)

    def FlushTime(self):
        
        """
        checks time and if its close tp midnight returns True
        """
        timelimit = 23*60.+ 45  # this is how many minutes are to 23:45
        #timelimit = 7*60.+ 40  # this is how many minutes are to 23:45
        
        b=  datetime.datetime.now()
        #fill in tuple
        a=b.timetuple()
        current_minute = a[3]*60. + a[4]
        if(current_minute > timelimit):
            return True
        else:
            return False
            
    def GetLatency(self):
        """determines latency from speedbox to  speed server
        retunrs the average
         """
        temp = measure_latency(host=self.latency_server , port=80, runs=10, timeout=2.5)
        #calculate average
        sum = 0.
        for k in range(0,len(temp)-1):
            sum = sum + temp[k]
        
        return sum/len(temp)
                 
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
        #return True
        #return True # part of debugging remove !!!!!!
        if( a.tm_min > 30 - temp) and ( a.tm_min < 30 + temp):
            return True
        else:
            #return False
            return False
        
        
        
        
            
    def RunShort(self):    
        process = sp.Popen(self.command,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         universal_newlines=True)
        
        out,err = process.communicate()
        
        print (out)
        sys.exit(0)
            
                    
    def Run(self):
        """
        this is the heart of the wrapper, using the CLI command
        """
        
        # here we do split
        if self.runmode == 'Both':
            if self.random_click :  # we switch randomly between runmodes
                if random.random() >.5 :
                    self.click = 1
                else:
                    self.click = 0
 
            if self.click == 1 :
                temp_runmode = 'Iperf'
                self.click = 0 # switch to opposite
            else:
                temp_runmode = 'Speedtest'
                self.click = 1
        else:
            temp_runmode = self.runmode

                
        

        # split bewteen iperf and speedtest
        if(temp_runmode == 'Iperf'):
            #self.SetupIperf3()

            print (self.command_iperf)
            process = sp.Popen(self.command_iperf,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         close_fds=True,
                         universal_newlines=True)
        
            out,err = process.communicate()
            print('error',err)
            print('runloop',out,type(out))
            self.CreateIperfOutput(out)
       # now create outputline from tuple
            myline=''
            for k in range(len(self.output)-1):
                myline=myline+str(self.output[k])+','
            myline = myline+str(self.output[len(self.output)-1])+'\n'
            print(myline)

        elif(temp_runmode == 'Speedtest'):
            process = sp.Popen(self.command_speed,
                         #stdout=outfile,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE,
                         close_fds=True,
                         universal_newlines=True)
        
            out,err = process.communicate()

            if process.returncode != 0:
                print("error",err)
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

            print(self.output)
            print(myline)
        else:
            print('Unknown Run Mode ',self.runmode, ' will exit')
            sys.exit(0)
        #check for date, we will open new file at midnight
        if(date.today()>self.current_day):
                #we have a new day
            self.output_file.close()
            self.OpenFile()
 
        
        if(self.Debug):
            self.myline = myline
            self.DebugProgram(3)
        print (myline)
        self.output_file.write(myline)
        self.output_file.flush() # to write to disk

    def CreateIperfOutput(self,iperfout): 
        """create output for iperf run"""  
        b=iperfout.replace('"','')
        b1=b.replace('\'','')
        c=b1.replace('[','')
        d=c.replace(']','')
        e=d.split(',')
        self.output=[]
        now=datetime.datetime.now()
 
        self.output = [now.strftime("%d/%m/%Y"),now.strftime("%H:%M:%S")]

        for k in [2,3,4]:
            try:
                self.output.append(e[k])
            except:
                print('no iperf')
                return
        for k in [5,6,11,8,9,10]:  # this funny e[11] ->e[7] has to do with the iperf3 system and what repesents download and what upload.
                                    # see link:https://github.com/esnet/iperf/issues/480##interpreting-the-results
            try:
                float(e[k])
                self.output.append(float(e[k]))
            except ValueError:

                print('bad float conversion')
                self.output.append(-10000.)
        return
            

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
        if(len(inc) == 12 ):  #this would be the case for the latest speetetst version
            inc.pop() #drop last
 
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
        #self.output.append(inc[0]) write out speedtest server name
        self.output.append("Speed")
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
        # now add the latency measurement 
        lat = self.GetLatency()
        self.output.append(lat)       
            
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
        self.SetDropDir() # determines the dropboxfolder
        
        self.input_path = homedir + '/speedfiles/'
        self.input_filename = filename
        filename = homedir + '/speedfiles/'+filename
        print (filename)
        self.lcwa_filename = filename
        if os.path.isfile(filename):
            self.output_file = open(filename,'a')
        else :
            self.output_file = open(filename,'w')
            self.WriteOutputHeader() # first time we write a header
            
        #Finally do the descriptor file
        self.WriteDescriptor()
            
            
    def WriteOutputHeader(self):       
        """
        Write the header for the output file
        """
        MyIP =self.DigIP()
        #Header = MyIP+',day,time,server name, server id,latency,jitter,package , download, upload , latency measured\n'
        Header = 'day,time,server name,server id,latency,jitter,package,download,upload,latency measured,'+MyIP+'\n'

        self.output_file.write(Header)
        
    def DebugProgram(self,err): 
        """
        Debug statements
        """
        temp = 'test_speed1_debug> '
        if(err == 1) :
            for k in range(len(self.ARGS)):
                print( temp,' cli commands',self.ARGS[k])
        elif(err ==2):
            print (temp, 'command for program ', self.command )
        elif(err ==3): 
            print (temp, 'Output :')
            print (self.myline)
        elif(err == 4):
            print( temp,'Data block',self.inc)
        elif(err == 5):
            print (temp,' output',self.output ) #for debugging
        elif(err==6):
            print (temp ,' my hostname ',self.hostname)
            #print (temp , 'my IP is '  , self.my_ip) 
            
    def DigIP(self):
        """ gets the ipaddress of the location"""
        
        stream = os.popen('dig +short myip.opendns.com @resolver1.opendns.com')
        return stream.read().strip('\n')
    
    def GetIPinfo(self):
        """
        gets the host info
        """
        a = socket.gethostname()
        #self.my_ip = socket.gethostbyname(a)
        
        # now chek the hostname if it is >4 characters strip rest
        # if it is shorter pad
        if len(a) > 4:
            self.hostname = a[:4]+'_'
            
        elif len(a) < 4:
            temp='xxxx'
            
            self.hostname = a+temp[0:4-len(a)]+'_' #pad with xxxx
        else:
            self.hostname = a+'_'
        
        if(self.Debug):
            self.DebugProgram(6)
        
        return
    
    def SoundAccoustic(self):
        #    give an audio signal that program is starting
        if platform.system() == 'Darwin':
            try:
                sp.call('/usr/local/bin/espeak " LCWA speedtest starting on Raspberry Pi"',shell=True)
            except:
                print( 'nospeak')
        elif platform.system() == 'Linux':
            try:
                sp.call('/usr/bin/espeak " LCWA speedtest starting on Raspberry Pi"',shell=True)
            except:
                print ('nospeak')

        
    def SetDropDir(self):
        """
        determines the directory on the dropbox according to the file name
        There are 10 LC directories LC01..LC10, for the currently envisioned number of raspis
        there is a ROTW (RestOfTheWorld), which takes all the other runs
        """
        #take the first 4 characters of the file
        a = self.docfile[0:5]
        print (a[0:2])
        if(a[0:2]=='LC'):
            self.dropdir = '/LCWA/'+a+'/'
        else:
            self.dropdir = '/LCWA/ROTW'+'/'
        print (self.dropdir)
        return 
    
    
    
    def DoPlots(self , textflag = False):  # textflag is set tru at midnight so that we dump statistics in txt file 
        """ this creates the plot and ships it to dropbox"""
        a =PC.MyPlot(self.input_path,self.input_filename,self.cryptofile,False)
        print(self.input_path,'   ', self.input_filename)
        temp_file = self.input_path+self.input_filename

        
        with open(temp_file) as f:
            count = 0
            for line in f:
                count += 1
        print (count)
        
        
        #count = len(open(temp_file).readlines(  ))
        if (count < 2):
            f.close()
            return 
        else:
            #f.close()
            
            a.ReadTestData()
            ##a.ConnectDropbox()
            ##a.PushFileDropbox(self.dropdir)

            print('dropbox dir for plot ',self.dropdir)
            temp = a.ReturnNames(self.dropdir)
 
            f=open(temp[1],"rb")
            temp1 = self.dbx.files_upload(f.read(),temp[0]+temp[2],mode=dropbox.files.WriteMode('overwrite', None))



            if textflag:
                a.Analyze(filename = self.textfile)
                f.close()
                return
            else:
                f.close()
                return
        
    def WriteDescriptor(self): 
        """ this writes a short descriptor file for the speedtest"""
        self.output_dict={'IP':self.DigIP(),
                          'Date':datetime.datetime.now(),
                          'Dropbox':self.dropdir, 
                          'MacAddress':self.Mac,
                          'File':self.docfile,
                          'version':self.vs,
                          'runmode': self.runmode}

        if self.runmode == "Iperf" or self.runmode == 'Both':
            self.output_dict.update({'iperf server': self.iperf_server,
                          'iperf port': self.iperf_port,
                          'iperf numstreams': self.iperf_numstreams,
                          'iperf blocksize': self.iperf_blksize,
                          'iperf duration': self.iperf_duration,
                          'iperf reverse' : self.iperf_reverse,
                          'time window' : self.loop_time})

        if self.runmode == "Speedtest" or self.runmode == 'Both':
            self.output_dict.update({
                         'ookla server id' : self.serverid,
                          'latency ip' : self.latency_server})

        if self.runmode  == "Both":
            self.output_dict.update({'random' : self.random_click})


        # Now print it
        self.textfile = self.lcwa_filename.replace('csv','txt')
        with open(self.textfile, 'w') as f:
        
        
            for key,value in self.output_dict.items():
                if key in self.output_dict.keys():
                    print(key , '  ',value, file = f)
            #print (self.output_dict['IP'])
        f.close()
           
    def GetMacAddress(self):
        """ gets the raspi mac address"""
 
        self.Mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
        for ele in range(0,8*6,8)][::-1]) 
    
    def CleanUpDropbox(self):
        """ this will check the dropbox folder for files that are older than a week and delete them"""
        
        self.dbx.files_delete(path, parent_rev)
        pass
 
    def Logging(self,message):
        """
        prints out erroro message with time
        """
        print(datetime.datetime.now(),' speedtest error > ',message)

    def SetupIperf3(self):

        """"instantiate the iperf client  for vs 7 and above"""
        print('setting up iperf client \n\n')
        self.myiperf = ipe.myclient(self.iperf_server,self.iperf_port,self.iperf_duration)
        self.myiperf.LoadParameters()
     
    
if __name__ == '__main__':
    
    server1 = 'speed-king.cybermesa.com:8080'
   # server1 = 'albuquerque.speedtest.centurylink.net:8080'
    ts = test_speed1(server=server1,chosentime=60)
    ts.GetArguments()  #commandline args
    ts.QueueRuntime()
    ts.OpenFile()  #output file
    
#    ts.GetArguments()
#    ts.OpenFile()
    ts.RunLoop()

    pass
