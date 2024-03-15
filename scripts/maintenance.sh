

 
# this file is run at the end of a git_pull
# so that any new push to the system beyond code is executed on the same night
#right now it is empty, but can be changed to adress new issues
#
echo "******************** this is the maintenance script ********************"

    pip3 install loguru
	
	echo $(pwd)
    # translating file

	#/Users/klein/git/speedtest/scripts/lcwa_dec.sh LCWA_translate
	#/home/pi/git/speedtest/scripts/lcwa_dec.sh /home/pi/git/speedtest/scripts/LCWA_translate
    #echo "finished translating"

