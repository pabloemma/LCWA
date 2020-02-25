#! /bin/sh
sudo -u pi -H sh -c "find /home/pi/speedtest -type f -name '*.csv' -mtime +2 -exec rm {} \; &"

