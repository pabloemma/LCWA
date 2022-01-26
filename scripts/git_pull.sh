#!

cd /home/pi/git/speedtest
echo $HOSTNAME

if [ ''$HOSTNAME'' = ''LC04'' ]; then
	echo "we are updating"
	cd ~/git/speedtest
    echo $PWD
	git pull
	git fetch
	git checkout test5
	cd /home/pi
	
	
else
	git pull
    cd /home/pi
fi


