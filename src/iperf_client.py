# this is a iperf3 clien script by ak
import iperf3 as ipe
from operator import itemgetter
import time

class myclient():

    def __init__(self,server_ip ,server_port, duration):
        # server_ip : address of iperf3 server
        # server_port: port to communicate; default 5021
        # duration : time of test, default 10 seconds
        # Instantiate the iperf3
        self.mycl = mycl = ipe.Client()



        # here we set up the communication parameters
        self.communication_dict={'duration':10,
        'protocol':'tcp',
        'blksize':1024,
        'json_output':True, #False: Terminal output, True Json output
        'num_streams':10,
        'verbose':False
        } 







        #establish connection tcp:
        mycl.server_hostname = self.server_ip = server_ip
        mycl.port = self.server_port = server_port
        
 

    def LoadParameters(self):
        
        #puts the iperf3 parameters into the client system
        # we loop over the communication dictionary

        for key,val in self.communication_dict.items():
            if( key == 'protocol'):
                self.mycl.protocol = val
            elif( key == 'blksize'):
                self.mycl.blksize = val
            elif( key == 'json_output'):
                self.mycl.json_output = val
            elif( key == 'duration'):
                self.mycl.duration = val
            elif( key == 'num_streams'):
                self.mycl.num_streams = val
            elif( key == 'verbose'):
                self.mycl.verbose = val

        print('protocol',self.mycl.protocol)        
            
            
            
      

    def RunTestTCP(self):
        # run the iperf test with tcp first
 
        result = self.mycl.run()
        print('result',result.system_info,'\n\n')
        print('protocol',result.protocol,'\n\n')
        print('Time',result.time)
        print('StartTime',result.timesecs)
        print('TX Mbps', result.sent_Mbps)
        print('RX Mbps',result.received_Mbps)

    def RunTestUDP(self):
        #Now run it with udp
                # here udp
        self.mycl1 = mycl1 = ipe.Client()
        self.mycl1.server_hostname = self.server_ip
        self.mycl1.server_port = self.server_port
        print('running udp \n\n\n')
        self.mycl1.protocol='udp'
        self.mycl1.blksize= 100000
        self.mycl1.num_streams= 2
        self.mycl1.duration= 5
        

        
 
        resultudp = self.mycl1.run()
        print('protocol',resultudp.protocol,'\n\n')

        print('jitter',resultudp.jitter_ms)
        print('packet',resultudp.packets)
        print('packet_loss',resultudp.lost_packets)
        print('packet loss in percent',resultudp.lost_percent)
        time.sleep(2)

    def SetValues(self,client_key,client_value):
        # sets value fo the dictionary for the iperf functions
        # 
        pass
if __name__ == '__main__':
    #server_ip = '63.229.162.245' #LCWA
    #server_port = 5201

    server_ip = '192.168.2.125' #"GH at LC20"
    server_port = 5201
    
    mycli = myclient(server_ip,server_port, duration=25)
    mycli.LoadParameters()
    mycli.RunTestTCP()
    mycli.RunTestUDP()
