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
from pathlib import Path



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

        self.DEBUG = False
 
        # read configuration
        self.read_config_file(config_file)
    
        self.file_name_beg = self.input_dir+'/'+self.speed_box+'_'
        self.file_name_end = 'speedfile.csv' 
        self.get_beginning_and_end()  # get the dates as date time


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
                self.input_dir = myconf['Input']['input_dir']

            if(self.speed_box == None):
                self.speed_box = myconf['Input']['speed_box']

            self.fmt                = myconf['Input']['fmt']
            #Math values
            # the rolling time window to average over
            self.rolling_time_window = int(myconf['Math']['rolling_time_window']) 
        return
    

    def loop_over_data_file(self):
        '''This is the main loop, over all the data files, we read in one file after the other'''

        # open first file and read into a panda structure
        temp_time = self.begin_time
        
        while True:
            inputfile = self.file_name_beg + temp_time + self.file_name_end

            #check if it , loop until we find it
            if (Path(inputfile).is_file):
                break
            else:
                temp_time = self.get_next_day(temp_time)
            
            if(dt.datetime.strptime(temp_time,self.fmt) > self.end_datetime):
                print("reached end of file list")
                return

        # now create first data frame
        data = pd.read_csv(inputfile,index_col=0,infer_datetime_format=True,parse_dates=True)

        # next we will be looping over all the other files in the time window
        # and adding them to the main data frame

       # get next day:
        next_day =  self.get_next_day(temp_time)
        
        while(dt.datetime.strptime(next_day,self.fmt) < self.end_datetime):
            try:
                inputfile = self.file_name_beg + next_day + self.file_name_end
                temp = pd.read_csv(inputfile,index_col=0,infer_datetime_format=True,parse_dates=True)
                if(self.DEBUG):
                    data.info()
                    temp.info()
                temp1=[data,temp]
                data = pd.concat(temp1)
                
                next_day =  self.get_next_day(next_day)
                
            except:
                next_day =  self.get_next_day(next_day)
                pass

        if(self.DEBUG):
            data.info()
        
        self.master_frame = data # we now deal with only one data frame




    def get_beginning_and_end(self):
        """the converts the first and last date into datetime"""
        self.beg_datetime = dt.datetime.strptime(self.begin_time,self.fmt)
        self.end_datetime = dt.datetime.strptime(self.end_time,self.fmt)

    def get_next_day(self,day):
        """calculates next day for file name, this to ensure that
        end of month is treated correctly"""
       
        
        temp_date = dt.datetime.strptime(day,self.fmt)
        new_day = temp_date + dt.timedelta(days = 1)

        # now convert back to string format
        
        return new_day.strftime(self.fmt)




if __name__ == "__main__":  
    config_file =  '/Users/klein/git/speedtest/config/PlotHistory.json'
    PH = PlotHistory(config_file = config_file , begin_time="2022-10-22",end_time = "2022-10-29")
    PH.loop_over_data_file()
   
