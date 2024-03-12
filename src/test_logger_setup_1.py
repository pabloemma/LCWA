import sys
import os
import json
import logging.config


# https://github.com/Delgan/loguru?tab=readme-ov-file

#import my_module

class MyLogger():
   
   
    def __init__(self,default_path=None):

        print("setup logging system")


    #def setup_logging(
    #    default_path=None,
    #    default_level=logging.INFO,
    #    env_key='LOG_CFG'
    #):
        """
        Setup logging configuration
        """
        path = default_path

        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
        else:
            print("can't find config file %s " %path)

        

        # now starts the hard work
        self.formatter_long = logging.Formatter('%(asctime)-16s  %(filename)-12s %(lineno)-6s %(funcName)-30s %(levelname)-8s %(message)s')
        self.formatter_short =    '[%(asctime)s] %(levelname)s %(message)s'
 
       
    def NewLogger(self, log_name, file_name, level=logging.INFO): 
        """ creates new logger for different levels"""
        if file_name == 'StreamHandler':
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(file_name)
        handler.setFormatter(self.formatter_long) 
        specified_logger = logging.getLogger(__name__)
        specified_logger.setLevel(level)
        specified_logger.addHandler(handler)
        specified_logger.propagate = False
        #logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))
        return specified_logger


    def CreateInfoLogger(self):
        global logger_ii
        logger_ii = self.NewLogger('info','StreamHandler',level = logging.INFO)
        logger_ii.info('stremahandler')

    def TestWarning(self,file_warning=None):
        global logger_w
        #logger_w = self.NewLogger('warning',file_warning,level = logging.INFO)

 
        logger_w = self.NewLogger('warning',file_warning,level = logging.WARNING)
        logger_w.warning("this is a warning")

    def TestInfo(self,file_info = None):
        global logger_i
        logger_i = self.NewLogger('info',file_info,level = logging.INFO)
        logger_i.info("this is an info")
        #logger_i.info("this is an info")
        logger_w.warning("this is now the second warning")

 
  



    
if __name__ == '__main__':
    dir = '/Users/klein/git/speedtest/config/'
    file = 'logger.json'
    MyPath = dir+file
    file_info = 'infotest.txt'
    file_warning = 'warningtest.txt'

    MyL=MyLogger(default_path=MyPath)
    MyL.CreateInfoLogger()
    MyL.TestWarning(file_warning =  file_warning)
    MyL.TestInfo(file_info = file_info)
