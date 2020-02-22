### BEGIN INIT INFO for raspi startup
# Provides:          run_speedtest.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

/home/pi/git/speedtest/src/test_speed1.py -t 10 -d /home/pi/git/speedtest/src/LCWA_d.txt -s 18002
