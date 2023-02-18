'''
Filename: /Users/klein/git/LCWA/src/PlotHistory.py
Path: /Users/klein/git/LCWA/src
Created Date: Saturday, February 18th 2023, 11:16:50 am
Author: Andi Klein

Copyright (c) 2023 panda woodworking

version 0.1
'''

import pandas as pd
import json 
import datetime as dt



class PlotHistory(object):

    def __init__(self,config_file , begin_time = None,end_time = None, input_dir = None, speed_box = None):
        ''' begin_time : starting date of time series
            end_time    :   end date
            dir         : backup directory
            
            '''
        self.begin_time = begin_time # format has to be of the form yyyy-mm-dd
        self.end_time = end_time
        self.input_dir = input_dir
        self.speed_box = speed_box

        # read configuration
        self.read_config_file(config_file)
    

    def read_config_file(self,config_file):
        '''reads in the json control file'''


        print("reading config file ", config_file)    
        with open(config_file, "r") as f:
            
            myconf = json.load(f)
    
            if(self.begin_time == None):
                self.begin_time = myconf['Input']['begin_time']

            if(self.end_time == None):
                self.end_time = myconf['Input']['end_time']

            if(self.input_dir == None):
                self.input_dir = myconf['Input']['end_time']

            if(self.speed_box == None):
                self.speed_box = myconf['Input']['speed_box']

            #Math values
            # the rolling time window to average over
            self.rolling_time_window = int(myconf['Math']['rolling_time_window']) 
        return
    

    def loop_over_data_file(self):
        '''This is the main loop, over all the data files, we read in one file after the other'''

        # open first file and read into a panda structure



    def get_next_day(sefl,day):
        '''calculates next day for file name, this to ensure that
        end of month is treated correctly'''
       
        fmt = "%Y-%m-%d"
        
        temp_date = dt.datetime.strptime(day,fmt)
        new_day = temp_date + dt.timedelta(days = 1)

        # now convert back to string format
        
        return new_day.strftime(fmt)


