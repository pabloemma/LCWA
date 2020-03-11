

'''
Created on Feb 8, 2020

@author: klein


This class is based on a packet sniffer code from
https://www.binarytides.com/python-packet-sniffer-code-linux/

The plan is to use it with the test_speed to debug LCWA speedissues
'''

import socket


class PacketSniff():
    
    
    def __init__(self):
        
    #establish a socket
        self.so = s =socket.socket( socket.AF_INET , socket.SOCK_RAW ,  socket.IPPROTO_TCP) 
        s.settimeout(0.0)
    # receive a packet
        while True:
            print s.recvfrom(65565)

if __name__ == '__main__':
    
    PS=PacketSniff()
