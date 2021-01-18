
#!/bin/bash



if [ $(ps -efa | grep -v grep | grep test_speed1_3.py -c) -gt 0 ] ;
then
    echo "Process running ...";
else

python3 -u /home/pi/git/speedtest/src/test_speed1_3.py -t 10 -d /home/pi/git/speedtest/src/LCWA_d.txt -s 18002  > /home/pi/run_speedtes_restart.log 2>> /home/pi/run_speedtest_restart_error.log &


echo "Starting the process";
fi;
