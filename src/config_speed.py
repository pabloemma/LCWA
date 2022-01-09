"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os
import sys
import platform


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for speedtest program"""


       
        
        # Open config file
        print('Directory Name:     ', os.path.dirname(__file__))
       

        if os.path.exists(config_file) :
            self.ReadJson(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)

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

    # now we read in the variables which are crucial for running
    # first we determine if we are running iperf or speedtest

        if(jsondict["Control"]["runmode"] == 'Iperf'):
            self.runmode = 'iperf'
            self.serverip = jsondict["Iperf"]["serverip"]
            self.serverport = jsondict["Iperf"]["port"]
            self.iperf_numstreams = jsondict["Iperf"]["numstreams"]
            self.iperf_blksize = jsondict["Iperf"]["blksize"]
            self.iperf_duration = jsondict["Iperf"]["duration"]
            if(jsondict["Iperf"]["reverse"]== 'True'):
                self.iperf_reverse = True
            else:
                self.iperf_reverse =  False

            
            
        elif (jsondict["Control"]['runmode'] == 'Speedtest'):
            self.runmode = 'speedtest'
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
        if(self.runmode == 'iperf'):
            
            print(' Running ',bfb,self.runmode,bfe,'  mode  \n')
            print('IP of server       ',self.serverip)
            print('Port               ',self.serverport)
            print('Duration           ',self.iperf_duration)
            print('Block size         ',self.iperf_blksize)
            print('Number of streams  ',self.iperf_numstreams)
            
            print('running reverse    ',self.iperf_reverse)

        else:
                print(' Running ',self.runmode,'  mode  \n')
        

        print('***************************** end of configuration***************\n\n')








if __name__ == '__main__':

    conf_dir = '/Users/klein/visual studio/LCWA/config/'
    config_file = conf_dir + 'test_speed_cfg.json'
    MyC = MyConfig(config_file)
