#! /bin/sh
sudo -u pi -H sh -c "find /home/pi/speedfiles -type f -name '*.csv' -mtime +2 -exec rm {} \; &"

