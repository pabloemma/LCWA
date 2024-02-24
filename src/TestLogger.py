'''
This is the logger class for test_speed1_3
author andi klein
Feb 2024

This is a work in progress :)

'''

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

    def __init__(self,LogFile = None, LogLevel= None, Output = None )
        

 


if __name__ == '__main__':
    TL = TestLogger(LogFile = ' test.log' , LogLevel = 1 , Output = 'both')