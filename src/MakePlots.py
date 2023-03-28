'''
Created on May 2, 2020

@author: klein
'''
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
import numpy as np
import csv
import time
import sys
import os.path
import dropbox

class MakePlots(object):
    '''
    classdocs
    '''


    def __init__(self, filename=None):
        '''
        Constructor
        '''
        self.filename=filename
        
    def ReadCSVFile(self,filenam=None):
        """
        reads in the csv file 
        """
    
        
        #We just check how many lines the files has.
        # need this to initialize the numpy arrays
        temp_file = open('temp.txt',"w")
        counter = 0

        if (filenam==None) :
            filename=self.filename
        else:
            self.filename=filename=filenam       
        with open(filename) as f:
            for i, l in enumerate(f):
                a=l.split(',')
                #print(l)
                if(len(a)< 9):
                    print ('problem',a)
                    print ('ignore data point at line ',counter+1)
                else:
                    
                    temp_file.write(l)
                    counter = counter + 1
            lines=counter-1
            temp_file.close()
                
                
                
 
 
        
        x0 =np.zeros(lines)
        xti=np.zeros(lines)
        y1=np.zeros(lines)
        y2=np.zeros(lines)
        format_file = "%d/%m/%Y %H:%M:%S"

         
        print('filename',filename)
        
        #  fille the arrays
        with open('temp.txt',newline='') as csvfile:
            spamreader = csv.reader(x.replace('\0', '') for x in csvfile)
            #spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            k=0
            for  row in spamreader:
                #print(', '.join(row))
                #print(row[0],row[7])  
                #print(len(row))
                if(k>0):
                    date_str = row[0]+' '+row[1]
                    try:
                        temp = time.mktime(datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S").timetuple())
                        #print(temp)
                    except: 
                        print("problems with file",self.filename)
                        continue
                        
                    aa =md.date2num(datetime.datetime.strptime(date_str,format_file))
                    x0[k-1] = aa
                    xti[k-1] = temp # for root time
                    y1[k-1] = row[7]
                    y2[k-1] = row[8]
                #print(x0[k-1] , '  ',y1[k-1])

            #print(aa)
                k=k+1
        self.x0 = x0
        self.y1 = y1
        self.y2 = y2
        self.xti = xti
        
        return [self.xti , self.y1,self.y2]
        
        
    def MakeThePlots(self):
        """ creates the Plots 
        """
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        y1=self.y1
        y2=self.y2
        plt.plot_date(self.x0,self.y1,'bs',label='\n blue DOWN ',markersize =2)
        plt.plot_date(self.x0,self.y2,'g^',label=' green UP',markersize =2)
#plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)
        #print(self.x0)
        ax.xaxis.set_major_locator(md.MinuteLocator(interval=1440))
        ax.xaxis.set_major_formatter(md.DateFormatter('%d/%m/%y %H:%M'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')
        
        plt.title('Speedtest LCWA using '+self.filename)
        print(' mean',np.around(np.mean(y1),2))
        plt.legend(facecolor='ivory',loc="upper left",shadow=True, fancybox=True)
 
        if(np.around(np.mean(y1),2) >25.): 
            plt.ylim(0.,70.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 25. and np.around(np.mean(y1),2) > 21.):
            plt.ylim(0.,41.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 21. and np.around(np.mean(y1),2) > 12.):
            plt.ylim(0.,24.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 12. and np.around(np.mean(y1),2) > 7.):
            plt.ylim(0.,12.) # set yaxis limit
             # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 7. ):
            plt.ylim(0.,7.) # set yaxis limit

#        I am taking out variable ylimits and replace it with hardwired of 22.
        #plt.ylim(0.,24.)


        plt.xticks(rotation='vertical')
        plt.tight_layout()
        self.file2 = file2 = self.filename.replace('csv','pdf')

        print (file2)
        fig.savefig(file2, bbox_inches='tight')
        #plt.show()





    
    def SaveFile(self):
        pass
    
if __name__ == '__main__':
    #create the list
    from pathlib import Path
    home = str(Path.home()) 
    
    File = home+'/scratch/LC04_2020-12-17speedfile.csv' 
    MP=MakePlots(File)
    MP.ReadCSVFile()
    MP.MakeThePlots() 

        
