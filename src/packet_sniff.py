

'''
Created on Feb 8, 2020

@author: klein


This class is based on a packet sniffer code from
https://www.binarytides.com/python-packet-sniffer-code-linux/

The plan is to use it with the test_speed to debug LCWA speedissues
'''

import socket
#import libpcap #needed for mac


class PacketSniff():
    
    
    def __init__(self):
        
        
        
        
    #establish a socket
    
        try:
            self.so = s =socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        except socket.error as msg:
            print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        s.settimeout(0.0)
        print (s)
        myHost = ''
        myPort = 50007
        self.so.bind((myHost,myPort))
    # receive a packet
        while True:
            self.so.listen(5)
            print(socket.gethostname())
            print( self.so.recvfrom(65565))

if __name__ == '__main__':
    
    PS=PacketSniff()
