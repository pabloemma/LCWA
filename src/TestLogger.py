'''
This is the logger class for test_speed1_3
author andi klein
Feb 2024

This is a work in progress :)

'''
import inspect

class TestLogger():

    """The Logger expects the filename to log to and the LogLevel;
    currently the levels are:
    info = 0
    lots_of_info = 1
    shitload of info = 2
    debug_1 = 4
    debug_2 = 5
    debug_3 = 6
    
    Output can be: screen,logfile,both

    """

    def __init__(self,LogFile = None, LogLevel= None, Output = None ):

        TX = color
        
        
        if(Output == 'logfile' or Output == 'both'):
            self.Openfile()
        else:
            frame = inspect.currentframe()
            prefix = TX.BOLD +TX.RED+'|'+frame.f_code.co_name+'>'+TX.END
            #print('\033[1m'+prefix)
            #print('test')



        print(prefix)

    #def OpenFile(self,LogFile)



class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

if __name__ == '__main__':
    TL = TestLogger(LogFile = ' test.log' , LogLevel = 1 , Output = 'screen')