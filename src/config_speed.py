"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os
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
        self.srcdir = jsondict['directory']['srcdir']
        self.datadir = jsondict['directory']['datadir']

        #these are depending on the operating system
        mysystem = platform.system()

        self.timeout = jsondict[mysystem]['timeout']
        self.speedtest = jsondict[mysystem]['speedtest']



        print('\n\n ***************** configuration**************\n')
        print(' We are running on platform ' , mysystem, '\n')

        print('Sourcedir            ',self.srcdir)
        print('Datadir              ',self.datadir)
        print('timeout command      ',self.timeout)
        print('speedtest command    ', self.speedtest)

        print('***************************** end of configuration***************\n\n')








if __name__ == '__main__':

    conf_dir = '/Users/klein/visual studio/LCWA/config/'
    config_file = conf_dir + 'test_speed_cfg.json'
    MyC = MyConfig(config_file)
