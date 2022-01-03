# needs to run as sudo since it sets the time of the machine
# we do this every midnight so that we can sync a few machines
import ntplib
import time
import os

def SetTime(self):
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time))) 
    except:
        print('Could not sync time with pool.ntp.org')