from socket import *
import os

def recvData(sock):
    data = ''
    try:
        print('1st')
        data = sock.recvfrom(65565)
        print('second')
    except OSError:
        data = ' '
        print ('socket error')
    return data[0]

def sniffing(host):
    if os.name == 'nt':
        sock_protocol = IPPROTO_IP
    else:
        #sock_protocol = IPPROTO_ICMP
        sock_protocol = 0
    sniffer = socket(AF_INET, SOCK_STREAM, sock_protocol)
    sniffer.bind((host, 1))
    sniffer.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    #sniffer.settimeout(0.0)
    sniffer.setblocking(0)
    if os.name == 'nt':
        sniffer.ioctl(SIO_RCVALL, RCVALL_ON)

    count = 1
    try:
        while True:
            print('in the loop')
            data = recvData(sniffer)
            print('after receive')
            print(data)
            print(str(count) + ' : ' + data[:20])
            count += 1
    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

def main():
    host = gethostbyname(gethostname())
    print("sniffing : " + host)
    sniffing(host)

if __name__ == "__main__":
  
    main()
