#!/bin/bash

COMMENT='#Every 10 Minutes, every hour of every day'
EVENT="*/10 * * * * /home/${USER}/git/speedtest/scripts/restart.sh"



# Check for root credentials

if [ "$(whoami)" != 'root' ]; then
echo "Error: root credentials required."
exit 1
fi

# Get the underlying use name:

UUSER="$(who am i | awk '{print $1}')"

if [ "$UUSER" = 'root' ]; then
echo "Error: this script must be run via sudo $0"
exit 1
fi


CRONTAB_FILE="/var/spool/cron/crontabs/${UUSER}"

if [ ! -f "$CRONTAB_FILE" ]; then
# Create a default crontab file..
echo "Creating crontab file for user ${UUSER}.."

cat >>"$CRONTAB_FILE" <<DEF1;
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
DEF1

fi

# Remove any old reference to the event..
SEARCHSTR="^.*$(basename "$EVENT" | sed -n -e 's/\./\\./gp').*$"
sed -i "/${SEARCHSTR}/d" "$CRONTAB_FILE"


echo "Adding ${EVENT} to ${CRONTAB_FILE}"
echo "$COMMENT" >>"$CRONTAB_FILE"
echo "$EVENT" >>"$CRONTAB_FILE"

echo 'New crontab:'
echo '======================================================================'
sudo -u "$UUSER" crontab -l
echo '======================================================================'
echo "Done."
