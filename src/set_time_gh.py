from datetime import datetime, timedelta                       # WGH mod
from os.path import exists                                     # WGH mod
import ntplib
import socket
import time



class MyTime():
    """this is run at the beginning when program starts up trying to
    do a crude sync of different machines, this way we might not hit the server all at the same time"""
  
    def __init__(self):
    
        self.cntp =ntplib.NTPClient()
 

    def GetTime(self):                                              # WGH mods

        """get time from ntp server"""

        # Retrieve list of ntp servers from /etc/systemd/timesyncd.conf
        # NTP=0.north-america.pool.ntp.org 1.north-america.pool.ntp.org 2.north-america.pool.ntp.org 3.north-america.pool.ntp.org
        NTPServers = None

        timesync_conf='/etc/systemd/timesyncd.conf'
        if exists(timesync_conf):
            file = open(timesync_conf, "r")
            for line in file:
                if line.startswith('NTP='):
                    line = line[4:]
                    NTPServers = line.split()
                    break
        
        if  NTPServers == None: # don't use None as false
            NTPServers = ["0.north-america.pool.ntp.org","1.north-america.pool.ntp.org","2.north-america.pool.ntp.org","3.north-america.pool.ntp.org"]

        # Reverse the order of the servers on the theory that the last is the least busy
        NTPServers = NTPServers[::-1]
            
        print('NTPServers: ', NTPServers)

        for ntpserver in NTPServers:
            try:
                self.ntp_response = self.cntp.request(ntpserver,version=3)
                print('Got time from ', ntpserver)
            except:
                self.ntp_received = False
                print('No NTP response from ', ntpserver)
                continue
            
            self.ntp_received = True
            
            print (datetime.fromtimestamp(self.ntp_response.tx_time))
            
            if(abs(self.ntp_response.offset) > 10):
                print('Warning: System time is not in sync with NTP.')
            
            print('System time offset from NTP:',self.ntp_response.offset)
            break

        return self.ntp_received

    def SetStart(self,hostname):                                        # WGH heavily modified
        # Calculates a wait seconds value so that LC01, LC02, etc. start in coordinated 25 second intervals.
        #   no matter what the individual time sync states are.
        #
        #   E.g. LC04 will start 100 seconds (1'40") past any 10 minute ntp clock mark, i.e. 00:11:40, 21:40, 31:40, etc.
        #   E.g. LC05 will start 125 seconds (2'05") past any 10 minute ntp clock mark, i.e. 00:12:05, 22:05, 32:05, etc.

        if not self.ntp_received:
            return 1
            
        hostnum = hostname[2:4]

        if not hostnum.isnumeric():
            print('hostname %s not numeric. Returning.' % hostname)
            return 1

        self.hostwait = int(hostnum) * 25

        # NTP Epoch time
        self.checktime = int(self.ntp_response.tx_time)
        
        # Uncomment the next block to enable test waiting only when the time is between 23:50:00 and 00:10:00

        # ~ # See if we're within 10 minutes either side of midnight
        # ~ self.last_midnight = self.checktime - (self.checktime % 86400) + time.timezone
        
        # ~ # Make sure last midnight is really in the past..
        # ~ if self.last_midnight > self.checktime:
            # ~ self.last_midnight -= 86400
        
        # ~ self.next_midnight = self.last_midnight + 86400
        
        # ~ print('         tz offset: ', time.timezone)
        # ~ print('    self.checktime: ', datetime.fromtimestamp(self.checktime))
        # ~ print('self.last_midnight: ', datetime.fromtimestamp(self.last_midnight))
        # ~ print('self.next_midnight: ', datetime.fromtimestamp(self.next_midnight))
        
        # ~ # Only set the wait queue if we're within 10 minutes before or after midnight
        
        # ~ if not ( self.checktime <= self.last_midnight + 600 or self.checktime >= self.next_midnight - 600 ):
            # ~ print('%s is not within our 20 minute wait-time window.  Returning.' % datetime.fromtimestamp(self.checktime))
            # ~ return 1

        self.runtime = self.checktime - (self.checktime % 600) + self.hostwait

        # Advance 10 minutes if runtime is in the past..
        if self.runtime < self.checktime:
            self.runtime += 600

        self.checktime = datetime.fromtimestamp(self.checktime)
        self.runtime = datetime.fromtimestamp(self.runtime)
#        self.waitsecs = (self.runtime - self.checktime).total_seconds()
        self.waitsecs = 1

        print('        Current NTP time: ', self.checktime)
        print('     Current System time: ', datetime.now())
        print('    Corrected sytem time: ', datetime.now()+timedelta(seconds=int(self.ntp_response.offset)))
        
        # Don't wait for hostname > LC24, i.e. don't wait for longer than 10 minutes, 25 seconds.
        if self.waitsecs > 625:
            print("%d seconds is too long to wait. Returning." % self.waitsecs)
            return False
        
        print('Setting runtime to (NTP): ', self.runtime)
        print('Setting runtime to (Sys): ', self.runtime-timedelta(seconds=int(self.ntp_response.offset)))
        print('                 Waiting:  %03d seconds.' % self.waitsecs)

        while(True):

            time.sleep(1)

            if(datetime.now()+timedelta(seconds=int(self.ntp_response.offset)) > self.runtime):
                print('Reached NTP run time of: ', self.runtime, ' at ', datetime.now(), ' system time.')
                break




if __name__ == '__main__':


    MT = MyTime()
    if MT.GetTime():                # WGH Mod
        MT.SetStart('miska')
