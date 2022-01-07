"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for speedtest program"""


       
        
        # Open config file

       

        if os.exists(config_file) :
            self.read_json(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)

        def read_json(file_path):

            print("reading config file")
            with open(file_path, "r") as f:
                return json.load(f)


if __name__ == '__main__':

    run_dir = speedtest/src/

    MyC = MyConfig(config_file)
