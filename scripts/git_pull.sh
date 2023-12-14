#!
# firts remove old log files
cd /home/pi
rm -v *.log

cd /home/pi/git/speedtest
echo $HOSTNAME

if [ ''$HOSTNAME'' = ''LC99'' ]; then
	echo "we are updating"
	cd ~/git/speedtest
    echo $PWD
	git pull
	git fetch
	git checkout test5
    cd src 
    ./update_speedtest
	cd /home/pi
	
	
else
	echo $(pwd)
	git pull
		

    cd /home/pi
	echo " taking a nap for things to settle"
	sleep 10
	echo "end nap"

	/home/pi/git/speedtest/scripts/maintenance.sh


fi


