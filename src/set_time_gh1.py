#!/usr/bin/env python3

import sys
# ~ import datetime
from datetime import datetime, timedelta                                # WGH mod
from os.path import exists                                              # WGH mod
import ntplib
import socket
import time
import os
import logging
from inspect import stack



class MyTime():
    """this is run at the beginning when program starts up trying to
    do a crude sync of different machines, this way we might not hit the server all at the same time"""
  
    def __init__(self, loop_time = 600, verbosity = 0):


        # create a module logger
        logger = logging.getLogger(__name__)

 
        # WGH mod: loop_time defines the wait time between speedtests.  Defaults to 10 minutes.
    
        self.loop_time = loop_time
        self.verbosity = verbosity
        # ~ self.cntp = ntplib.NTPClient()
 
    def GetNTPOffset(self, ntpserverarg = None):                                    # WGH mods
        # Queries a list of NTP servers for the offset from NTP time (which may be > 1 second 
        # ..if the systemd-timesyncd.service is improperly configured or not running.
        #
        # Sets self.ntp_received to True if the NTP query is successful and False if not.
        #
        # Returns a tuple: the value of self.ntp_response.offset, an expiration date for the ntp offset, 4 hours in the future
        # A 0 offset return indicates that the NTP queries failed.
        #

        self.ntp_offset = 0
        self.ntp_querytime = 0

        self.cntp = ntplib.NTPClient()
        
        """get time from ntp server"""

        NTPServers = None

        if ntpserverarg == None:
            # Retrieve list of ntp servers from /etc/systemd/timesyncd.conf

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

            # Prioritize LCWA's NTP server
            NTPServers.append("172.16.2.3")

            ################################################################
            # Use for DEBUGING tests of no response from any NTP servers..
            # NTPServers = ["6.north-america.pool.ntp.org","7.north-america.pool.ntp.org","8.north-america.pool.ntp.org","9.north-america.pool.ntp.org"]        
            ################################################################

            # Reverse the order of the servers on the theory that the last is the least busy
            NTPServers = NTPServers[::-1]
        else:
            NTPServers = [ ntpserverarg ]
        
        logging.info(('%-34s: %s' % ('NTPServers', NTPServers)))

        for ntpserver in NTPServers:
            try:
                
                logging.info(('%-34s: %s' % ('Querying NTP server', ntpserver)))
                self.ntp_response = self.cntp.request(ntpserver,version=3)
                logging.info(('%-34s: %s' % ('NTP query returned offset', self.ntp_response.offset)))
                
            except:
                self.ntp_received = False
                logging.warning(('Warning: no NTP response from %s' % ntpserver))
                continue
            
            self.ntp_received = True
            self.ntp_offset = self.ntp_response.offset
            self.ntp_querytime = int(time.time())
            
            if(abs(self.ntp_response.offset) > 10):
                logging.warning(('Warning: System time is out of sync with NTP by %d seconds.' % self.ntp_offset))
            else:
                logging.info(('%-34s: %s' % ('System time offset from NTP',self.ntp_offset)))
            break

        if self.ntp_received == False:
            logging.error(('Warning: All NTP queries unsuccessful.'))
            logging.warning(('Warning: Falling back to using system time without NTP offset.'))
        else:
            logging.info(('%-34s: %s' % ('NTP offset query time',datetime.fromtimestamp(self.ntp_querytime))))

        # A 0 return means that the ntp query was unsuccessful
        return self.ntp_offset, self.ntp_querytime

    def GetOffset(self):
        return self.ntp_offset

    def QueueWait(self,hostname = socket.gethostname(), ntp_offset = 0):                 # WGH heavily modified
        # Calculates a wait seconds value so that LC01, LC02, etc. start in coordinated 25 second intervals,
        #   no matter what the individual system time sync states are.
        #
        #   E.g. LC04 will start 100 seconds (1'40") past any 10 minute ntp clock mark, i.e. 00:11:40, 21:40, 31:40, etc.
        #   E.g. LC05 will start 125 seconds (2'05") past any 10 minute ntp clock mark, i.e. 00:12:05, 22:05, 32:05, etc.
        #
        #   WGH further mods so that SetStart just relies on system time if all GetTime() NTP queries have failed.
        #
        # Returns 1 == error, 0 == success

        hostnum = hostname[2:4]
        host = hostname[0:4]

        # If we're not an LCnn, just sleep the loop_time. Use the test_speed1_3.py --time arg to shorten the loop_time
        if not hostnum.isnumeric():
            logging.warning('Warning: hostname %s not numeric. Setting queue position to 0.' % hostname)
            hostnum = 0

        # Seconds after the self.loop_time intervals to wait until.
        #   The '25' multiplier is based on 24 active test units * 25 second window for each == 10 minutes
        self.hostwait = int(hostnum) * 25

        # If hostname is > LC24..
        if self.hostwait > self.loop_time:
            self.hostwait = (int(hostnum) % 25) * 25

        # And/or if we're operating with a short loop_time
        if self.hostwait > self.loop_time:
            self.hostwait = (int(hostnum) * 25) % self.loop_time    # This is for debugging..

        # DEBUGGING
        # ~ if hostnum == 99:
            # ~ self.hostwait = 0
            # ~ ntp_offset = 0
        
        # epoch time
        self.et_checktime = self.et_systime = int(time.time())

        # Correct for the ntp offset
        self.et_checktime += ntp_offset

        logging.info(('  %-32s: %s' % ('Current system time', datetime.fromtimestamp(self.et_systime))))
        if ntp_offset != 0: logging.info(('  %-32s: %s\n' % ('Corrected NTP time', datetime.fromtimestamp(self.et_checktime))))
    
        # Calculate the run window in ntp corrected time..
        et_runwindow_start = self.et_checktime - (self.et_checktime % self.loop_time) + self.loop_time
        et_runwindow_end   = et_runwindow_start + self.loop_time

        if ntp_offset != 0: logging.info(('  %-32s: %s' % ('NTP Run window start', datetime.fromtimestamp(et_runwindow_start))))
        if ntp_offset != 0: logging.info(('  %-32s: %s\n' % ('NTP Run window end', datetime.fromtimestamp(et_runwindow_end))))

        et_sysrunwindow_start = et_runwindow_start - ntp_offset
        et_sysrunwindow_end   = et_runwindow_end - ntp_offset

        logging.info(('  %-32s: %s' % ('Sys Run window start', datetime.fromtimestamp(et_sysrunwindow_start))))
        logging.info(('  %-32s: %s\n' % ('Sys Run window end', datetime.fromtimestamp(et_sysrunwindow_end))))
        

        # Calculate the time of the next speedtest as a corrected epoch time
        self.et_runtime = self.et_checktime - (self.et_checktime % self.loop_time) + self.hostwait

        # Advance by loop_time seconds if runtime is in the past..
        if self.et_runtime < self.et_checktime:
            self.et_runtime += self.loop_time

        self.et_sysruntime = self.et_runtime - ntp_offset

        self.et_waitsecs = self.et_runtime - self.et_checktime

        if self.verbosity > 0:
            if ntp_offset != 0: logging.info(('  %-32s: %s' % ('Next test time (NTP) for '+host, datetime.fromtimestamp(self.et_runtime))))
            logging.info(('  %-32s: %s' % ('Next test time (Sys) for '+host, datetime.fromtimestamp(self.et_sysruntime))))
        else:
            logging.info(('  %-32s: %s' % ('Scheduling next test runtime for', datetime.fromtimestamp(self.et_sysruntime))))
            
        logging.info(('  %-32s: %03d seconds..' % ('Waiting', self.et_waitsecs)))

        while(True):
            time.sleep(1)
            et_ntp_now = time.time() + ntp_offset

            # Show a countdown timer..
            #temp_txt = str('\r%66s' % int(self.et_runtime - et_ntp_now), end = ' ')
            #logging.info(temp_txt)

            if( et_ntp_now >= self.et_runtime ):
                break

        
        if ntp_offset != 0: logging.info(('  %-32s: %s' % ('NTP time now', datetime.fromtimestamp(self.et_runtime))))
        if ntp_offset != 0: logging.info(('  %-32s: %s\n' % ('Reached scheduled ntp runtime of', datetime.fromtimestamp(et_ntp_now))))

        logging.info(('  %-32s: %s' % ('System time now', datetime.fromtimestamp(et_ntp_now - ntp_offset))))
        logging.info(('  %-32s: %s' % ('Reached scheduled test runtime', datetime.fromtimestamp(et_ntp_now))))

        return 0

    def Logging(self,message, verbosity = 0):
        """
        prints out erroro message with time
        """
        # WGH mod: send any message with a verbosity < 0 or containing 'error'
        # or 'exception' to stderr, ..and include the file, function & lineno of the caller.
        # Messages with verbosity > self.verbosity are ignored.

        # if message contains just newlines or whitespace, print just the newlines/whitespace
        if message.isspace() == True:
            if verbosity < 0:
                print(message, flush=True, file=sys.stderr)
            else:
                print(message, flush=True)
        
        elif '_tostd_' in message and verbosity <= self.verbosity:
            message = message.replace('_tostd_', '')
            print(datetime.now(), message, flush=True)
        elif "error" in message.lower() or "exception" in message.lower() or verbosity < 0:
            # If message contains '_nostack_' don't print the mod def names and lineno..
            if "_nostack_" in message:
                message = message.replace('_nostack_', '')
                callerstr = ""
            else:
                calling_file = stack()[1][1]
                calling_func = stack()[1][3]
                calling_line = stack()[1][2]
                callerstr = " %s: %s, line %d " % (os.path.basename(calling_file), calling_func, calling_line)

            print(datetime.now(),
                  callerstr,
                  message,
                  flush=True, file=sys.stderr)
        elif "_toerr_" in message.lower():
            # If message contains '_toerr_' print the message to stderr
            message = message.replace('_toerr_', '')
            print(datetime.now(), message, flush=True, file=sys.stderr)
            
        elif verbosity <= self.verbosity:
            print(datetime.now(), message, flush=True)
        

if __name__ == '__main__':

    my_verbosity = 2
    my_loop_time = 60

    MT = MyTime( loop_time = my_loop_time, verbosity = my_verbosity)

    # GetNTPOffset returns a tuple!
    my_ntp_offset, my_ntp_expired = MT.GetNTPOffset()

    print('\n')

    print(datetime.now(),'GetNTPOffset returned %s, offset expires %s\n' % (my_ntp_offset, datetime.fromtimestamp(my_ntp_expired)))

    print(datetime.now(),'Testing QueueWait() ...')

    MT.QueueWait('LC01', ntp_offset = my_ntp_offset)
