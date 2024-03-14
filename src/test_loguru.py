# using the loguru logger
# need to do a pip3 install loguru
import sys
import os
import json

try:
    from loguru import logger
except:
    print('module not available')
# https://github.com/Delgan/loguru?tab=readme-ov-file

#import my_module

class MyLogger():

    def __init__(self, ConfPath = None , LogPath = None):

     
        #lets add output file for logger info
        #logger.add(LogPath, colorize = True,format="<green>{time}</green> <level>{message}</level>")
        logger.remove(0) # remove the standard
        self.ConfPath = ConfPath #currently not used

        #Path to where the logfile goes
        self.LogPath = LogPath

    def ConfigLogger(self):
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green> {level} <level>{message}</level>")



        fmt =  "{time} - {name}-{function} -{line}- {level} - {message}"
        logger.add(self.LogPath, format = fmt)


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        #logger.opt(ansi=True).info('<red>Logging System vs {} using loguru</red> ' ,1.0)

        logger.info('this is an info')
        logger.debug('this is debug')
        logger.warning('this is a warning')
        logger.error('this is an error')






if __name__ == '__main__':



    conf_dir = '/Users/klein/git/speedtest/config/'
    conf_file = 'logger.json'
    ConfPath = conf_dir+conf_file
    log_dir = '/Users/klein/git/speedtest/log/'
    log_file = 'loguru.txt'
    LogPath = log_dir+log_file
    MyL=MyLogger(ConfPath=ConfPath, LogPath=LogPath)
    MyL.ConfigLogger()

   