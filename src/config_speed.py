"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os
import sys
import platform
import socket


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for speedtest program"""


       
        
        # Open config file
        print('Directory Name:     ', os.path.dirname(__file__))
       

        if os.path.exists(config_file) :
            self.ReadJson(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)
            sys.exit(0)
    def ReadJson(self,file_path):

        print("reading config file")
        with open(file_path, "r") as f:
            myconf = json.load(f)

            self.DecodeVariables(myconf)

    def DecodeVariables(self,jsondict):
        """decodes the json dictionary in to variables"""

        #bold face begin and end
        bfb = '\033[1m'
        bfe = '\033[0m'
        #these are depending on the operating system
        mysystem = platform.system()
        self.srcdir = jsondict[mysystem]['srcdir']
        self.datadir = jsondict[mysystem]['datadir']

        self.timeout = jsondict[mysystem]['timeout']
        self.speedtest = jsondict[mysystem]['speedtest']

        self.debug = jsondict["Control"]["debug"]
        self.cryptofile = jsondict["Control"]["cryptofile"]
        # the next two vaiables are only used if we run in "both" mode
        self.click      = jsondict["Control"]["click"] # 1: start with iperf, 0 start with speedtest
        self.random_click     = jsondict["Control"]["random"]


        self.conf_dir = jsondict[mysystem]['conf_dir']

    # now we read in the variables which are crucial for running
    # first we determine if we are running iperf or speedtest
    # this depends on the ClusterControl entry

        self.runmode = self.GetClusterVariables(jsondict)

        if(self.runmode == 'Iperf'):
            self.iperf_serverip = jsondict["Iperf"]["serverip"]
            self.iperf_serverport = jsondict["Iperf"]["serverport"]
            self.iperf_numstreams = jsondict["Iperf"]["numstreams"]
            self.iperf_blksize = jsondict["Iperf"]["blksize"]
            self.iperf_duration = jsondict["Iperf"]["duration"]
            self.latency_ip = jsondict["Iperf"]["latency_ip"]
            self.time_window =      jsondict["Iperf"]["time_window"]

            if(jsondict["Iperf"]["reverse"]== True):
                self.iperf_reverse = True
            else:
                self.iperf_reverse =  False

            
        elif (self.runmode == 'Speedtest'):
            self.latency_ip =       jsondict["Speedtest"]["latency_ip"]
            self.serverip =         jsondict["Speedtest"]["serverip"]
            self.serverid =         jsondict["Speedtest"]["serverid"]
            self.time_window =      jsondict["Speedtest"]["time_window"]



        elif (self.runmode ==   'Both'):
            self.iperf_serverip = jsondict["Iperf"]["serverip"]
            self.iperf_serverport = jsondict["Iperf"]["serverport"]
            self.iperf_numstreams = jsondict["Iperf"]["numstreams"]
            self.iperf_blksize = jsondict["Iperf"]["blksize"]
            self.iperf_duration = jsondict["Iperf"]["duration"]
            self.latency_ip = jsondict["Iperf"]["latency_ip"]
            self.time_window =      jsondict["Iperf"]["time_window"]
            if(jsondict["Iperf"]["reverse"]== True):
                self.iperf_reverse = True
            else:
                self.iperf_reverse =  False
            self.latency_ip =       jsondict["Speedtest"]["latency_ip"]
            self.serverip =         jsondict["Speedtest"]["serverip"]
            self.serverid =         jsondict["Speedtest"]["serverid"]
            self.time_window =      jsondict["Speedtest"]["time_window"]



        else:
            print('that runmode is unknown',jsondict["Control"]['runmode'] )
            sys.exit()

        print('\n\n ***************** configuration**************\n')
        print(' We are running on platform ' , mysystem, '\n')

        print('Sourcedir            ',self.srcdir)
        print('Datadir              ',self.datadir)
        print('timeout command      ',self.timeout)
        print('speedtest command    ', self.speedtest)
        print('\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!     run parameters \n')
        if(self.runmode == 'Iperf'):
            
            print(' Running ',bfb,self.runmode,bfe,'  mode  \n')
            print('IP of server       ',self.iperf_serverip)
            print('Port               ',self.iperf_serverport)
            print('Duration           ',self.iperf_duration)
            print('Block size         ',self.iperf_blksize)
            print('Number of streams  ',self.iperf_numstreams)
            
            print('running reverse    ',self.iperf_reverse)

        elif(self.runmode == 'Speedtest'):
            print(' Running ',bfb,self.runmode,bfe,'  mode  \n')
            print('Latency server       ',self.latency_ip)
            print('Server IP            ',self.serverip)
            print('Server ID            ',self.serverid)
            print('times intervals      ',self.time_window)
        
        elif(self.runmode == 'Both'):
            print(' Running ',bfb,self.runmode,bfe,'  mode  \n')
            print('IP of server       ',self.iperf_serverip)
            print('Port               ',self.iperf_serverport)
            print('Duration           ',self.iperf_duration)
            print('Block size         ',self.iperf_blksize)
            print('Number of streams  ',self.iperf_numstreams)
            
            print('running reverse    ',self.iperf_reverse)
            #print(' Running ',bfb,self.runmode,bfe,'  mode  \n')
            print('Latency server       ',self.latency_ip)
            print('Server IP            ',self.serverip)
            print('Server ID            ',self.serverid)
            print('times intervals      ',self.time_window)

            
 
        print('***************************** end of configuration***************\n\n')


    def GetClusterVariables(self,jsondict):
        """determines the cluster run parameter for the different boxes"""

        # get hostname
        host = socket.gethostname()
        if host in jsondict["ClusterControl"].keys():
           return jsondict["ClusterControl"][host]

        else:  
           return 'Both'
 






if __name__ == '__main__':

    conf_dir = '/home/klein/git/speedtest/config/'
    config_file = conf_dir + 'test_speed_cfg.json'
    MyC = MyConfig(config_file)
