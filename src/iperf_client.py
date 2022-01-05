# this is a iperf3 clien script by ak
import iperf3 as ipe  #iperf3 library, does not allow for multiple connections

#from pyperf2 import Server, Client  # this would be with iperf2
from operator import itemgetter
import datetime as dt
import time
# for argument parser
import argparse as argp
import sys
import socket

class myclient():

    def __init__(self):
        # server_ip : address of iperf3 server
        # server_port: port to communicate; default 5021
        # duration : time of test, default 10 seconds
        # Instantiate the iperf3
        self.output =output = []
        self.time_sleep = 1
 


 






       
    def GetArguments(self):
        """get host ip, port and other arguments
        iperfhost : server ip address
        iperfport ; server port
        duration : legth
        numstreams ;  number of streams; careful too many loads down the cpu
        
        """
        #right now it is only pass
        #instantiate the parser

        iperf_parser = argp.ArgumentParser(description='cli for iperf')
        iperf_parser.add_argument("-s","--serverip",help = "Specify server ip" )
        iperf_parser.add_argument("-p","--serverport",help = "Specifyserver port " )
        iperf_parser.add_argument("-d","--duration",help = "Specify duration of iperf" )
        iperf_parser.add_argument("-n","--numstream",help = "Specify numberof streams" )
        iperf_parser.add_argument("-b","--blksize",help = "Specify block size" )
        iperf_parser.add_argument("-dd","--debug",action='store_true',help = "debug system")
        iperf_parser.add_argument("-r","--reverse",action='store_true',help = "run iperf in reverse mode")
        iperf_parser.add_argument("-v","--verbose",action='store_true',help = "verbose mode")
        #iperf_parser.add_argument("-h","--help",action='store_true',help = "print out menu")
        iperf_parser.add_argument("-j","--json",action='store_true',help = "json output")

        iperf_parser.add_argument("-gp","--getport",action='store_true',help = "get port according to host name")


    # get the arguments
        args = iperf_parser.parse_args()

       # we need to give it default values
        #self.server_ip = '63.229.162.245'
        self.server_ip = '192.168.2.125'
        self.server_port = 5201
        self.duration = 10
        self.numstream = 1
        self.blksize = 100000
        self.debug = False
        self.reverse = False
        self.verbose = False
        self.json_output = True


        # here we deal with the arguments.
        if(args.serverip != None) :
            self.server_ip = args.serverip

        if(args.serverport != None):
            self.server_port = args.serverport

        if(args.duration != None):
            self.duration = int(args.duration)

        if(args.numstream != None):
            self.numstream = int(args.numstream)

        if(args.blksize != None):
            self.blksize = int(args.blksize)

        if(args.debug ):
            self.debug = args.debug
  
        if(args.verbose ):
            self.verbose = args.verbose

        if(args.reverse ):
            self.reverse = args.reverse
 
        if(args.json ):
            self.json_outpout = args.json

        if(args.getport):
            self.GetPort() # get port number according to speedbox name
 
      
        

        # now let's print out the configuration if we debug
        
        if self.debug:
            print('\n\n **********************  this is the iperf client ****************** \n\n')
            print('server host   ',self.server_ip)
            print('server port   ',self.server_port)
            print('Duration      ',self.duration)
            print('Num streams   ', self.numstream)
            print('Blocksize     ',self.blksize)
            print('Verbose     ',self.verbose)
            print('Reverse     ',self.reverse)
            print('Json Output ',self.json_output)
            print('\n\n **********************  this is the iperf client ****************** \n\n')
 
        return


             
            
      

    def RunTestTCP(self):
        # run the iperf test with tcp first
        self.mycl = mycl = ipe.Client()
        
        dummy = 'xxxx'
        self.mycl.server_hostname = self.server_ip
        self.mycl.port = self.server_port

        print(self.server_port,'****')

        self.mycl.verbose = self.verbose
        self.mycl.json_output = self.json_output
        self.mycl.num_streams = self.numstream
        self.mycl.duration = self.duration
        self.mycl.blksize = self.blksize
        self.mycl.reverse = self.reverse


        output = self.output
        result = self.mycl.run()
        output.append(dt.datetime.fromtimestamp(result.timesecs).strftime('%d/%m/%Y'))
        output.append(dt.datetime.fromtimestamp(result.timesecs).strftime('%H:%M:%S'))
        output.append('iperf3')
        output.append(dummy)
        output.append(dummy)
        output.append('0') # jitter
        output.append('0') #package loss
        output.append(result.received_Mbps)
        output.append(result.sent_Mbps)
        output.append('0')
        


        if(self.debug):
            self.PrintResults(result)
        
        time.sleep(self.time_sleep)
        return 

    def RunTestUDP(self):
        #Now run it with udp
                # here udp
        self.mycl1 = mycl1 = ipe.Client()
        self.mycl1.server_hostname = self.server_ip
        self.mycl1.server_port = self.server_port
        #print('running udp \n\n\n')
        self.mycl1.protocol='udp'
        self.mycl1.json_output = self.json_output
        self.mycl1.num_streams = self.numstream
        self.mycl1.duration = self.duration
        self.mycl1.blksize = self.blksize
        self.mycl1.reverse = self.reverse
        

        
 
        resultudp = self.mycl1.run()
        self.output.append(resultudp.jitter_ms)
        self.output.append(resultudp.packets)
        self.output.append(resultudp.lost_percent)
        time.sleep(self.time_sleep)
 
        return 

    def GetPort(self):
        """Determine port according to host name"""
        self.hostname = socket.gethostname()
        
        if self.hostname[:2] == 'LC':
            temp = int(self.hostname[2:4])
            if ( temp == 4):
                self.server_port = 5201
                return
            else:
                print('not a recognized speedbox, exiting')
                sys.exit()
        else:
            print('Not implemented hostname')
            sys.exit()


    def PrintResults(self,result):
        """called in debug mode, provides more infor"""
        print('\n\n\n********************************  more info *************************\n\n')
        print('Total local CPU Load        ',result.local_cpu_total)
        print('local user CPU Load         ',result.local_cpu_user)
        print('local system CPU Load       ',result.local_cpu_system)
        print('Total remote CPU Load        ',result.local_cpu_total)
        print('remote user CPU Load         ',result.local_cpu_user)
        print('remote system CPU Load       ',result.local_cpu_system)
        print('\n*************************************************************************\n\n')

    def SetReverse(self):
        """this sets the reverse to opposite the previous value and then we run again
        so if you start with reverse now it will make a regular connection """
        if(self.reverse):
            self.reverse = False
        else:
            self.reverse = True

    def CreateOutput(self):
        """parses the output and creates a new one for the test_speed program"""
        print(len(self.output))
        temp1=[]
        for k in range (0,7):
            temp1.append(self.output[k])
        for k in range (20,26):
            temp1.append(self.output[k])
        print(temp1)
        if self.debug:
            print(' full output from tcp and udp both regular and reverse \n\n')
            print(self.output)
        return self.output

    def EndClient(self):
        quit()
if __name__ == '__main__':
    import time
 
    mycli = myclient()
    mycli.GetArguments()
    mycli.RunTestTCP()
    mycli.RunTestUDP()
    mycli.SetReverse()
    mycli.RunTestTCP()
    mycli.RunTestUDP()
    mycli.CreateOutput()
 
 
        
 
