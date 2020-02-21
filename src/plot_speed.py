#!/usr/bin/env python

'''
Created on Jan 23, 2020

@author: klein
'''



import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import csv
import time
import sys
import os.path
import dropbox

drop = False
#for k in range(len(sys.argv)):
#    print sys.argv

if len(sys.argv)==2:
    # check if file exists
    try:
        os.path.isfile((sys.argv[1]))
        filename = sys.argv[1]
        file1=filename
    except:
        print('no file')
        sys.exit(0)
elif len(sys.argv)==3:
    drop=True
    

else:
    print( ' to run the program you have to give a filename \n plot_speed.py inputfile ')
    print(' You have to give the token file')
    sys.exit(0)
    
# connect to dropbox
if(drop):
    f=open(sys.argv[2],"r")
    data =f.readline() #key for encryption
    data=data.strip('\n')

#connect to dropbox
    dbx=dropbox.Dropbox(data)
    myaccount = dbx.users_get_current_account()
    print('***************************dropbox************************************')
    print('*                                                                    *')
    print 'first = ',myaccount.name.given_name,'last = ',myaccount.name.surname  
    print 'email account = ',myaccount.email
    print('*                                                                    *')
    print('***************************dropbox************************************')

# get dropbox file

    file = '/LCWA/'+ sys.argv[1]
    dir = os.path.expanduser("~")
    file1 = dir+'/scratch/'+sys.argv[1]
    filename = dbx.files_download_to_file(file1,file)
    #print filename         
x1 = []
y1 = []
x2 = []
y2 =[]

# check for data integrtity by writing file to temporary buffer

temp_file = open('temp.txt',"w")
counter = 0
for line in open(file1, 'r'):

    a = line.split(',')
    if(len(a)< 9):
        print ('problem',a)
        print ('ignore data point at line ',counter+1)
    else:
        temp_file.write(line)
    counter = counter + 1
#file1.close()
temp_file.close()
   


#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"        
x1,y1,y2 = np.loadtxt('temp.txt', delimiter=',',
                   unpack=True,usecols=(1,7,8),
#        converters={ 1: md.strpdate2num('%d/%m/%Y-%H:%M:%S')})
        converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        #converters={ 0: md.strpdate2num('%d/%m/%Y')})


np.set_printoptions(precision=2)
fig=plt.figure() 
ax=fig.add_subplot(1,1,1)
ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)
ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)

plt.plot_date(x1,y1,'g^',label='\n green UP ')
plt.plot_date(x1,y2,'bs',label=' blue DOWN')
#plt.text(1.,1.,r' $\sigma = .1$')
plt.grid(True)

ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
plt.xlabel('Time')
plt.ylabel('Speed in Mbs')
if(drop):
    plt.title('Speedtest LCWA using '+file)
else:
    plt.title('Speedtest LCWA using '+file1)
    
plt.legend(facecolor='ivory',loc="lower right",shadow=True, fancybox=True)
plt.ylim(0.,24.) # set yaxis limit
plt.xticks(rotation='vertical')
plt.tight_layout()
file2 = file1.replace('csv','pdf')

print file2
fig.savefig(file2, bbox_inches='tight')
plt.show()



if __name__ == '__main__':
    pass