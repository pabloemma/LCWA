from datetime import  date , datetime , timezone, timedelta
import ntplib
import socket


class MyTime():
  """this is run at the beginning when program starts up trying to
  do a crude sync of different machines, this way we might not hit the server all at the same time"""
  
  def __init__(self):
    
    self.cntp =ntplib.NTPClient()
 

  def GetTime(self):

        """get time from ntp server and then sync with it"""
        
        response = self.cntp.request('us.pool.ntp.org',version = 3)
        if(abs(response.offset) < 10):
          print("we have less thhan 20 sec time walk")
        else:
          print('need to sync time')

        print('timedifference  ',response.offset)
        self.mytime = datetime.fromtimestamp(response.tx_time)
        print (datetime.fromtimestamp(response.tx_time))

  def SetStart(self,hostname):

    temp = hostname
    #temp = socket.gethostname()
 
    MyNumber = int(temp[2:4])*25

 
    while(True):
 
      #print(datetime.now())
      if(datetime.now() > self.mytime+timedelta(0,MyNumber)):
        print('reached start time at', datetime.now())        
        break




if __name__ == '__main__':


  MT = MyTime()
  MT.GetTime()
  MT.SetStart('LC04')
