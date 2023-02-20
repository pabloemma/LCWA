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
import matplotlib.pyplot as plt
import matplotlib.dates as md



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
            self.outfile                = myconf['Input']['outfile']
            
            #Math values
            # the rolling time window to average over
            self.rolling_time_window = int(myconf['Math']['rolling_time_window']) 
            
            
            # properties of the database
            self.drop_columms = myconf['DB']['drop_columns'] # columns to be dropped from the database
            #self.drop_columns = []
            self.plot_columns = myconf['DB']['plot_columns']
            self.rolling_points = int(myconf['DB']['rolling_points'])

            #plot control
            self.y_bottom_limit = float(myconf['Plot']['y_bottom_limit'])
            self.y_top_limit = float(myconf['Plot']['y_top_limit'])

        return
    

    def loop_over_data_file(self):
        '''This is the main loop, over all the data files, we read in one file after the other'''

        # open first file and read into a panda structure
        temp_time = self.begin_time
        
        while True:
            inputfile = self.file_name_beg + temp_time + self.file_name_end

            #check if it , loop until we find it
            if (Path(inputfile).is_file()):
                break
            else:
                temp_time = self.get_next_day(temp_time)
            
            if(dt.datetime.strptime(temp_time,self.fmt) > self.end_datetime):
                print("reached end of file list")
                return

        # now create first data frame
        data = pd.read_csv(inputfile)
        if(self.DEBUG):
            print(data.head())
        #now drop the columns we don't need:
        data.drop(self.drop_columms, axis=1, inplace=True)

        # next we will be looping over all the other files in the time window
        # and adding them to the main data frame

       # get next day:
        next_day =  self.get_next_day(temp_time)
        
        while(dt.datetime.strptime(next_day,self.fmt) < self.end_datetime):
            try:
                inputfile = self.file_name_beg + next_day + self.file_name_end
                temp = pd.read_csv(inputfile)
                temp.drop(self.drop_columms, axis=1, inplace=True)

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

       #convert time to datetime
        self.master_frame["Time"] = pd.to_datetime(self.master_frame['day']+self.master_frame['time'],format='%d/%m/%Y%H:%M:%S')
        if(self.DEBUG):
            print(self.master_frame.head())

        #create rolling mean
        self.master_frame["Rolling_up"] = self.master_frame.upload.rolling(self.rolling_points).mean()
        self.master_frame["Rolling_down"] = self.master_frame.download.rolling(self.rolling_points).mean()


        #save master frame 
        self.master_frame.to_csv('/Users/klein/scratch/testplot.csv')
        if(self.DEBUG):
            print(self.master_frame.head())

 
    


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



    def plot_speed_old(self):
        """plots the up and download"""

        fig = plt.figure()
        ax=fig.add_subplot(1,1,1)
        #ax.text(.05,.95,'iperf and ookla on'+' '+self.DigIP(),weight='bold',transform=ax.transAxes,fontsize=11)

        #ax.xaxis.set_major_locator(md.MinuteLocator(interval=6000))
        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')

        #plt.title('Speedtest LCWA '+self.InputFile)



    
        #plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["download"],'bs',label='\n iperf blue DOWN ')
        #plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["upload"],'g^',label='\n iperf green UP ')
        #plt.plot(self.master_frame["Time"],self.master_frame["download"],'ks',label='\n speedtest black DOWN ')
        #plt.plot(self.master_frame["Time"],self.master_frame["upload"],'r^',label='\n speedtest red UP ')
        #plt.plot(self.master_frame["Time"],self.master_frame["upload"],color='green',linestyle='-',label='\n speedtest red UP ')
        #plt.plot(self.master_frame["Time"],self.master_frame["download"],color='red',linestyle='-',label='\n speedtest red UP ')
        plt.plot(self.master_frame["Time"],self.master_frame["Rolling_up"],color='green',linestyle='-',label='\n speedtest green DOWN ')
        plt.plot(self.master_frame["Time"],self.master_frame["Rolling_down"],color='red',linestyle='-',label='\n speedtest red UP ')
        
        # remove limit
        plt.ylim(bottom = 0.)
        plt.grid(True)

        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True,fontsize = 6)
 
        #print (self.output)
        
        fig.savefig(self.outfile, bbox_inches='tight')

    
        plt.show()


    def plot_speed(self):
        """plots the up and download"""

        fig = plt.figure()
        axe = []
        axe.append(fig.add_subplot(2,2,4))
        axe.append(fig.add_subplot(2,2,3))
        axe.append(fig.add_subplot(2,2,2))
        axe.append(fig.add_subplot(2,2,1))
        #ax.text(.05,.95,'iperf and ookla on'+' '+self.DigIP(),weight='bold',transform=ax.transAxes,fontsize=11)

       
            #axe[k].set_xticks(rotation='vertical')
            #axe[k].tight_layout()
            #axe[k].legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True,fontsize = 6)

        #plt.title('Speedtest LCWA '+self.InputFile)



    
        #plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["download"],'bs',label='\n iperf blue DOWN ')
        #plt.plot(self.lcwa_iperf["Time"],self.lcwa_iperf["upload"],'g^',label='\n iperf green UP ')
        #plt.plot(self.master_frame["Time"],self.master_frame["download"],'ks',label='\n speedtest black DOWN ')
        #plt.plot(self.master_frame["Time"],self.master_frame["upload"],'r^',label='\n speedtest red UP ')
        axe[2].plot(self.master_frame["Time"],self.master_frame["Rolling_up"],color='green',linestyle='-',label='\n speedtest green DOWN ')
        axe[3].plot(self.master_frame["Time"],self.master_frame["Rolling_down"],color='red',linestyle='-',label='\n speedtest red UP ')
        axe[0].plot(self.master_frame["Time"],self.master_frame["upload"],color='green',linestyle='-',label='\n speedtest red UP ')
        axe[1].plot(self.master_frame["Time"],self.master_frame["download"],color='red',linestyle='-',label='\n speedtest red UP ')
        
        # remove limit
         #ax.xaxis.set_major_locator(md.MinuteLocator(interval=6000))

        #for xticks
        #first determine how many x tenries we have
        x_spread = self.master_frame.shape[0]
        # now we just want 6 ticks
        interval = int(x_spread/6)
        x_ticks = self.master_frame["Time"][::interval]
        for k in range(0,4):
            axe[k].tick_params('x',labelrotation = 45.)
            axe[k].set_xticks(x_ticks)
            axe[k].xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
            axe[k].set_xlabel('Time')
            axe[k].set_ylabel('Speed in Mbs')
            axe[k].set_ylim(bottom = self.y_bottom_limit,top = self.y_top_limit)
            axe[k].grid(True)


        plt.tight_layout()


        #plt.legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True,fontsize = 6)
 
        #print (self.output)
        
        fig.savefig(self.outfile, bbox_inches='tight')

    
        plt.show()





    



if __name__ == "__main__":  
    config_file =  '/Users/klein/git/speedtest/config/PlotHistory.json'
    PH = PlotHistory(config_file = config_file , begin_time="2022-11-22",end_time = "2023-01-12")
    PH.loop_over_data_file()
    PH.plot_speed()
   
